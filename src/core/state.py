"""
State management for MCP-based requirement processing.

This module provides a StateManager class for managing state files
that track the progress of requirement implementation across LLM sessions.
"""

import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from core.config import ROOT_DIR

# State constants
STATE_IDLE = "IDLE"
STATE_VALIDATING = "VALIDATING"
STATE_RUN_CREATED = "RUN_CREATED"
STATE_IMPLEMENTING = "IMPLEMENTING"
STATE_VERIFYING = "VERIFYING"
STATE_READY_TO_FINALIZE = "READY_TO_FINALIZE"
STATE_COMPLETED = "COMPLETED"
STATE_FAILED = "FAILED"

# Valid state transitions
VALID_TRANSITIONS = {
    STATE_IDLE: [STATE_VALIDATING],
    STATE_VALIDATING: [STATE_RUN_CREATED, STATE_FAILED],
    STATE_RUN_CREATED: [STATE_IMPLEMENTING],
    STATE_IMPLEMENTING: [STATE_VERIFYING, STATE_FAILED],
    STATE_VERIFYING: [STATE_READY_TO_FINALIZE, STATE_IMPLEMENTING, STATE_FAILED],
    STATE_READY_TO_FINALIZE: [STATE_COMPLETED],
    STATE_COMPLETED: [],  # Terminal state
    STATE_FAILED: [STATE_IDLE],  # Can retry from IDLE
}

# State directory
STATE_DIR = os.path.join(ROOT_DIR, "00_SYSTEM", "state")


class StateManager:
    """Manages state files for requirement processing."""

    def __init__(self, req_id: str):
        """Initialize state manager for a specific requirement.
        
        Args:
            req_id: The requirement ID (e.g., "REQ-MCP-001")
        """
        self.req_id = req_id
        self.state_file = os.path.join(STATE_DIR, f"{req_id}.json")
        self._ensure_state_dir()

    def _ensure_state_dir(self) -> None:
        """Ensure the state directory exists."""
        if not os.path.exists(STATE_DIR):
            os.makedirs(STATE_DIR)

    def _now(self) -> str:
        """Get current timestamp in ISO format."""
        return datetime.now().isoformat()

    def exists(self) -> bool:
        """Check if state file exists."""
        return os.path.exists(self.state_file)

    def load(self) -> Optional[Dict[str, Any]]:
        """Load state from file.
        
        Returns:
            State dict if exists, None otherwise.
        """
        if not self.exists():
            return None
        with open(self.state_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self, state: Dict[str, Any]) -> None:
        """Save state to file.
        
        Args:
            state: State dict to save.
        """
        state["updated_at"] = self._now()
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)

    def create(self) -> Dict[str, Any]:
        """Create a new state file with IDLE state.
        
        Returns:
            The newly created state dict.
        """
        now = self._now()
        state = {
            "req_id": self.req_id,
            "run_id": None,
            "state": STATE_IDLE,
            "created_at": now,
            "updated_at": now,
            "history": [],
            "last_error": None,
            "disc_path": None,
        }
        self.save(state)
        return state

    def get_or_create(self) -> Dict[str, Any]:
        """Get existing state or create new one.
        
        Returns:
            The state dict.
        """
        state = self.load()
        if state is None:
            state = self.create()
        return state

    def get_state(self) -> str:
        """Get current state value.
        
        Returns:
            Current state string, or IDLE if no state file.
        """
        state = self.load()
        if state is None:
            return STATE_IDLE
        return state.get("state", STATE_IDLE)

    def can_transition(self, from_state: str, to_state: str) -> bool:
        """Check if a state transition is valid.
        
        Args:
            from_state: Current state.
            to_state: Target state.
            
        Returns:
            True if transition is valid.
        """
        valid_targets = VALID_TRANSITIONS.get(from_state, [])
        return to_state in valid_targets

    def transition(
        self,
        to_state: str,
        run_id: Optional[str] = None,
        error: Optional[Dict[str, Any]] = None,
        disc_path: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Transition to a new state.
        
        Args:
            to_state: Target state.
            run_id: Optional run ID to set.
            error: Optional error info to record.
            disc_path: Optional discussion path for failures.
            
        Returns:
            Updated state dict.
            
        Raises:
            ValueError: If transition is invalid.
        """
        state = self.get_or_create()
        from_state = state["state"]

        if not self.can_transition(from_state, to_state):
            raise ValueError(
                f"Invalid state transition: {from_state} -> {to_state}. "
                f"Valid transitions from {from_state}: {VALID_TRANSITIONS.get(from_state, [])}"
            )

        # Record history
        state["history"].append({
            "from": from_state,
            "to": to_state,
            "timestamp": self._now(),
            "run_id": run_id or state.get("run_id"),
        })

        # Update state
        state["state"] = to_state
        if run_id is not None:
            state["run_id"] = run_id
        if error is not None:
            state["last_error"] = error
        if disc_path is not None:
            state["disc_path"] = disc_path

        # Clear error on successful transitions (except FAILED)
        if to_state not in [STATE_FAILED] and error is None:
            state["last_error"] = None

        self.save(state)
        return state

    def set_error(self, error: Dict[str, Any], disc_path: Optional[str] = None) -> Dict[str, Any]:
        """Set error information without changing state.
        
        Args:
            error: Error information dict.
            disc_path: Optional discussion path for the error.
            
        Returns:
            Updated state dict.
        """
        state = self.get_or_create()
        state["last_error"] = error
        if disc_path is not None:
            state["disc_path"] = disc_path
        self.save(state)
        return state

    def reset(self) -> Dict[str, Any]:
        """Reset state to IDLE (for retrying after failure).
        
        Returns:
            Reset state dict.
        """
        state = self.get_or_create()
        if state["state"] != STATE_FAILED:
            raise ValueError(f"Can only reset from FAILED state, current: {state['state']}")
        
        state["history"].append({
            "from": state["state"],
            "to": STATE_IDLE,
            "timestamp": self._now(),
            "run_id": state.get("run_id"),
            "action": "reset",
        })
        
        state["state"] = STATE_IDLE
        state["run_id"] = None
        state["last_error"] = None
        # Keep disc_path for reference
        
        self.save(state)
        return state

    def delete(self) -> bool:
        """Delete state file.
        
        Returns:
            True if deleted, False if didn't exist.
        """
        if self.exists():
            os.remove(self.state_file)
            return True
        return False


def get_next_action(state: Dict[str, Any]) -> Dict[str, Any]:
    """Determine the next action based on current state.
    
    Args:
        state: Current state dict.
        
    Returns:
        Dict with next_action and any relevant parameters.
    """
    current = state["state"]
    req_id = state["req_id"]
    run_id = state.get("run_id")
    
    if current == STATE_IDLE:
        return {
            "next_action": "call apply_req",
            "description": f"Start processing {req_id} by calling apply_req('{req_id}')",
        }
    
    elif current == STATE_VALIDATING:
        return {
            "next_action": "wait",
            "description": "Validation in progress, wait for result",
        }
    
    elif current == STATE_RUN_CREATED:
        return {
            "next_action": "implement",
            "description": f"Implement the requirement as specified in the RUN file",
            "run_id": run_id,
        }
    
    elif current == STATE_IMPLEMENTING:
        return {
            "next_action": "call continue_req",
            "description": f"Continue implementation by calling continue_req('{req_id}')",
        }
    
    elif current == STATE_VERIFYING:
        return {
            "next_action": "verify",
            "description": "Run verification (tests, lint) and report results",
        }
    
    elif current == STATE_READY_TO_FINALIZE:
        return {
            "next_action": "call finalize_run",
            "description": f"Finalize by calling finalize_run('{run_id}')",
            "run_id": run_id,
        }
    
    elif current == STATE_COMPLETED:
        return {
            "next_action": "done",
            "description": f"Requirement {req_id} has been completed successfully",
        }
    
    elif current == STATE_FAILED:
        error = state.get("last_error", {})
        disc_path = state.get("disc_path")
        return {
            "next_action": "handle_failure",
            "description": "Review error and decide whether to retry or create discussion",
            "error": error,
            "disc_path": disc_path,
            "retry_hint": "Call apply_req again after fixing issues to retry",
        }
    
    return {
        "next_action": "unknown",
        "description": f"Unknown state: {current}",
    }


def list_active_states() -> List[Dict[str, Any]]:
    """List all active (non-completed) state files.
    
    Returns:
        List of state summaries.
    """
    if not os.path.exists(STATE_DIR):
        return []
    
    results = []
    for filename in os.listdir(STATE_DIR):
        if filename.endswith(".json"):
            filepath = os.path.join(STATE_DIR, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    state = json.load(f)
                if state.get("state") != STATE_COMPLETED:
                    results.append({
                        "req_id": state.get("req_id"),
                        "state": state.get("state"),
                        "run_id": state.get("run_id"),
                        "updated_at": state.get("updated_at"),
                    })
            except (json.JSONDecodeError, IOError):
                continue
    
    return results
