import argparse
import asyncio
import inspect
from typing import Any, Dict, Optional

try:
    from fastmcp import FastMCP
except ImportError:  # pragma: no cover
    class FastMCP:
        def tool(self):
            def decorator(func):
                return func
            return decorator

mcp = FastMCP()

from core.automation import Automator
from core.checks import check_links, check_requirements, check_structure, doctor, lint_metadata
from core.config import ROOT_DIR


@mcp.tool()
def apply_req(
    req_id: str,
    dry_run: Optional[bool] = False,
    create_spec: Optional[object] = "auto",
) -> Dict[str, Any]:
    """
    Start or resume REQ processing with state machine.
    
    Idempotent: Safe to call multiple times. Returns current state if already in progress.
    
    Args:
        req_id: Target REQ ID (e.g., "REQ-VALID-001")
        dry_run: Preview only, no actual changes
    
    Returns:
        State-aware response with:
        - state: Current state
        - next_action: What to do next
        - run_id: RUN ID if created
        - errors: List of validation errors (if any)
        - disc_path: Discussion path (if failed)
    """
    from core.state import (
        StateManager, 
        STATE_IDLE, STATE_VALIDATING, STATE_RUN_CREATED, STATE_FAILED,
        get_next_action
    )
    
    sm = StateManager(req_id)
    state = sm.get_or_create()
    current = state["state"]
    
    # Idempotent: if already past IDLE, return current state
    if current not in [STATE_IDLE, STATE_FAILED]:
        next_action = get_next_action(state)
        return {
            "state": current,
            "req_id": req_id,
            "run_id": state.get("run_id"),
            "next_action": next_action["next_action"],
            "description": next_action["description"],
            "message": f"Already in progress. Current state: {current}",
        }
    
    # If FAILED, reset to IDLE first
    if current == STATE_FAILED:
        state = sm.reset()
    
    # Transition to VALIDATING
    state = sm.transition(STATE_VALIDATING)
    
    # Run validation
    automator = Automator()
    errors = []
    
    # Check REQ exists and is valid
    if not automator.validate_req(req_id):
        errors.append({
            "type": "req_validation",
            "message": str(automator.last_error),
            "retry_from": "apply_req",
        })
    
    # Run lint check
    lint_issues = lint_metadata(ROOT_DIR)
    if lint_issues > 0:
        errors.append({
            "type": "lint",
            "message": f"{lint_issues} lint issues found",
            "retry_from": "apply_req",
        })

    # Run requirements check
    req_issues = check_requirements(ROOT_DIR)
    if req_issues > 0:
        errors.append({
            "type": "requirements",
            "message": f"{req_issues} requirement issues found",
            "retry_from": "apply_req",
        })

    # Run links check
    link_issues = check_links(ROOT_DIR)
    if link_issues > 0:
        errors.append({
            "type": "links",
            "message": f"{link_issues} link issues found",
            "retry_from": "apply_req",
        })
    
    # If validation failed, transition to FAILED
    if errors:
        disc_path = None
        if not dry_run:
            try:
                context = {
                    "req_id": req_id,
                    "stage": "validate",
                    "errors": errors,
                }
                disc_path = automator.create_disc_from_context(context)
                disc_path = str(disc_path)
            except Exception:
                pass
        
        state = sm.transition(
            STATE_FAILED,
            error={"errors": errors},
            disc_path=disc_path,
        )
        
        return {
            "state": STATE_FAILED,
            "req_id": req_id,
            "errors": errors,
            "disc_path": disc_path,
            "next_action": "fix_errors",
            "description": "Fix the errors listed above, then call apply_req again",
        }
    
    # Validation passed, create RUN
    if dry_run:
        return {
            "state": STATE_VALIDATING,
            "req_id": req_id,
            "dry_run": True,
            "message": "Validation passed. Would create RUN (dry_run=True)",
            "next_action": "call apply_req with dry_run=False",
        }
    
    # Create RUN and transition to RUN_CREATED
    create_spec_mode = create_spec
    if isinstance(create_spec_mode, str) and create_spec_mode.lower() == "auto":
        create_spec_mode = automator._requires_spec(req_id)
    if create_spec_mode not in (True, False):
        create_spec_mode = True
    spec = (
        automator.create_spec_draft(req_id, dry_run=False)
        if create_spec_mode
        else None
    )
    run_path = automator.create_run(req_id, spec_path=spec)
    run_id = run_path.stem if hasattr(run_path, 'stem') else str(run_path).split("/")[-1].replace(".md", "")
    
    state = sm.transition(STATE_RUN_CREATED, run_id=run_id)
    next_action = get_next_action(state)
    
    return {
        "state": STATE_RUN_CREATED,
        "req_id": req_id,
        "run_id": run_id,
        "run_path": str(run_path),
        "next_action": next_action["next_action"],
        "description": next_action["description"],
    }


@mcp.tool()
def apply_req_full(
    req_id: str,
    dry_run: Optional[bool] = False,
) -> Dict[str, Any]:
    """
    One-shot orchestration for REQ processing via the state machine.
    
    The MCP does not edit code; it returns instructions and follow-up hints
    so the client/agent can implement changes and then resume verification.
    """
    from core.state import (
        StateManager,
        STATE_IDLE,
        STATE_VALIDATING,
        STATE_RUN_CREATED,
        STATE_IMPLEMENTING,
        STATE_VERIFYING,
        STATE_READY_TO_FINALIZE,
        STATE_COMPLETED,
        STATE_FAILED,
        get_next_action,
    )

    sm = StateManager(req_id)
    state = sm.get_or_create()
    current = state["state"]
    run_id = state.get("run_id")
    automator = Automator()

    def _finalize_from_state(run_id_value: str, success: bool = True) -> Dict[str, Any]:
        archived_path = automator.finalize_run(run_id_value, success=success)
        if success:
            state_now = sm.load()
            if state_now and state_now.get("state") == STATE_READY_TO_FINALIZE:
                sm.transition(STATE_COMPLETED, run_id=run_id_value)
            return {
                "state": STATE_COMPLETED,
                "req_id": req_id,
                "run_id": run_id_value,
                "archived_path": str(archived_path),
                "next_action": "done",
                "description": "Run finalized successfully. Requirement implementation complete.",
            }
        sm.transition(
            STATE_FAILED,
            run_id=run_id_value,
            error={"errors": [{"type": "finalization", "message": "Run marked as failed"}]},
        )
        return {
            "state": STATE_FAILED,
            "req_id": req_id,
            "run_id": run_id_value,
            "archived_path": str(archived_path),
            "next_action": "fix_errors",
            "description": "Run finalized as failed. Review errors and retry.",
        }

    if dry_run:
        next_action = get_next_action(state)
        return {
            "state": current,
            "req_id": req_id,
            "run_id": run_id,
            "dry_run": True,
            "next_action": next_action["next_action"],
            "description": next_action["description"],
            "message": "dry_run=True; no state changes or writes performed.",
        }

    if current == STATE_FAILED:
        state = sm.reset()
        current = state["state"]
        run_id = state.get("run_id")

    if current == STATE_IDLE:
        state = sm.transition(STATE_VALIDATING)
        errors = []

        if not automator.validate_req(req_id):
            errors.append({
                "type": "req_validation",
                "message": str(automator.last_error),
                "retry_from": "apply_req_full",
            })

        lint_issues = lint_metadata(ROOT_DIR)
        if lint_issues > 0:
            errors.append({
                "type": "lint",
                "message": f"{lint_issues} lint issues found",
                "retry_from": "apply_req_full",
            })

        req_issues = check_requirements(ROOT_DIR)
        if req_issues > 0:
            errors.append({
                "type": "requirements",
                "message": f"{req_issues} requirement issues found",
                "retry_from": "apply_req_full",
            })

        link_issues = check_links(ROOT_DIR)
        if link_issues > 0:
            errors.append({
                "type": "links",
                "message": f"{link_issues} link issues found",
                "retry_from": "apply_req_full",
            })

        if errors:
            disc_path = None
            try:
                context = {
                    "req_id": req_id,
                    "stage": "validate",
                    "errors": errors,
                }
                disc_path = automator.create_disc_from_context(context)
                disc_path = str(disc_path)
            except Exception:
                pass

            sm.transition(STATE_FAILED, error={"errors": errors}, disc_path=disc_path)
            return {
                "state": STATE_FAILED,
                "req_id": req_id,
                "errors": errors,
                "disc_path": disc_path,
                "next_action": "fix_errors",
                "description": "Fix the errors listed above, then call apply_req_full again.",
            }

        create_spec_mode = automator._requires_spec(req_id)
        spec = (
            automator.create_spec_draft(req_id, dry_run=False)
            if create_spec_mode
            else None
        )
        run_path = automator.create_run(req_id, spec_path=spec)
        run_id = run_path.stem if hasattr(run_path, "stem") else str(run_path).split("/")[-1].replace(".md", "")

        state = sm.transition(STATE_IMPLEMENTING, run_id=run_id)
        return {
            "state": STATE_IMPLEMENTING,
            "req_id": req_id,
            "run_id": run_id,
            "run_path": str(run_path),
            "next_action": "implement",
            "description": "Implement the requirement as specified in the RUN file.",
            "instructions": "Apply code changes, then call apply_req_full again to verify and finalize.",
            "continue_with": "apply_req_full",
            "continue_args": {"req_id": req_id},
        }

    if current == STATE_RUN_CREATED:
        state = sm.transition(STATE_IMPLEMENTING, run_id=run_id)
        return {
            "state": STATE_IMPLEMENTING,
            "req_id": req_id,
            "run_id": state.get("run_id"),
            "next_action": "implement",
            "description": "Implement the requirement as specified in the RUN file.",
            "instructions": "Apply code changes, then call apply_req_full again to verify and finalize.",
            "continue_with": "apply_req_full",
            "continue_args": {"req_id": req_id},
        }

    if current == STATE_IMPLEMENTING:
        if not run_id:
            run_id = automator._format_run_id(req_id)
        sm.transition(STATE_VERIFYING, run_id=run_id)
        issues = doctor(ROOT_DIR)
        if issues > 0:
            errors = [{"type": "doctor", "message": f"{issues} doctor issue(s) found"}]
            sm.transition(STATE_IMPLEMENTING, error={"errors": errors}, run_id=run_id)
            return {
                "state": STATE_IMPLEMENTING,
                "req_id": req_id,
                "run_id": run_id,
                "errors": errors,
                "next_action": "fix_errors",
                "description": "Fix validation errors, then call apply_req_full again.",
                "instructions": "Apply fixes, then call apply_req_full to re-verify.",
                "continue_with": "apply_req_full",
                "continue_args": {"req_id": req_id},
            }
        sm.transition(STATE_READY_TO_FINALIZE, run_id=run_id)
        return _finalize_from_state(run_id)

    if current == STATE_VERIFYING:
        if not run_id:
            run_id = automator._format_run_id(req_id)
        issues = doctor(ROOT_DIR)
        if issues > 0:
            errors = [{"type": "doctor", "message": f"{issues} doctor issue(s) found"}]
            sm.transition(STATE_IMPLEMENTING, error={"errors": errors}, run_id=run_id)
            return {
                "state": STATE_IMPLEMENTING,
                "req_id": req_id,
                "run_id": run_id,
                "errors": errors,
                "next_action": "fix_errors",
                "description": "Fix validation errors, then call apply_req_full again.",
                "instructions": "Apply fixes, then call apply_req_full to re-verify.",
                "continue_with": "apply_req_full",
                "continue_args": {"req_id": req_id},
            }
        sm.transition(STATE_READY_TO_FINALIZE, run_id=run_id)
        return _finalize_from_state(run_id)

    if current == STATE_READY_TO_FINALIZE:
        if not run_id:
            run_id = automator._format_run_id(req_id)
        return _finalize_from_state(run_id)

    if current == STATE_COMPLETED:
        return {
            "state": STATE_COMPLETED,
            "req_id": req_id,
            "run_id": run_id,
            "next_action": "done",
            "description": f"{req_id} has been completed successfully.",
        }

    next_action = get_next_action(state)
    return {
        "state": current,
        "req_id": req_id,
        "run_id": run_id,
        "next_action": next_action.get("next_action", "unknown"),
        "description": next_action.get("description", f"Unknown state: {current}"),
    }


@mcp.tool()
def create_run(req_id: str) -> Dict[str, Any]:
    """
    Create a RUN document from template for a REQ.
    
    Args:
        req_id: Target REQ ID
    
    Returns:
        Dict with run_path
    """
    automator = Automator()
    if not automator.validate_req(req_id):
        raise ValueError(f"REQ validation failed: {automator.last_error}")
    run_path = automator.create_run(req_id)
@mcp.tool()
def intake(description: str, domain: str = "GEN") -> Dict[str, Any]:
    """
    Intake a new user request and create a BRIEF document.
    
    Args:
        description: The user's raw request or description.
        domain: Domain code (default "GEN").
    
    Returns:
        Dict with brief_path.
    """
    automator = Automator()
    path = automator.intake(description, domain)
    return {"brief_path": str(path)}


@mcp.tool()
def plan(brief_id: str) -> Dict[str, Any]:
    """
    Create a RUN document from an existing BRIEF.

    This is the main planning function in the 3-Step Workflow:
    1. Intake -> Creates BRIEF
    2. Plan (this) -> Creates RUN from BRIEF
    3. Finish -> Marks RUN as completed

    Args:
        brief_id: The ID of the Brief (e.g., "BRIEF-MCP-003").

    Returns:
        Dict with run_id and run_path.
    """
    automator = Automator()
    path = automator.plan(brief_id)
    return {"run_id": path.stem, "run_path": str(path)}


@mcp.tool()
def plan_from_brief(brief_id: str) -> Dict[str, Any]:
    """
    Alias for plan() - kept for backward compatibility.

    Args:
        brief_id: The ID of the Brief (e.g., "BRIEF-GEN-001").

    Returns:
        Dict with run_id and run_path.
    """
    return plan(brief_id)


@mcp.tool()
def continue_req(req_id: str, implementation_done: Optional[bool] = False) -> Dict[str, Any]:
    """
    Continue REQ processing based on current state.
    
    This is the main state-machine driver. Call this after completing each step.
    
    Args:
        req_id: Target REQ ID
        implementation_done: Set True when implementation is complete
    
    Returns:
        State-aware response with next action to take.
    """
    from core.state import (
        StateManager,
        STATE_RUN_CREATED, STATE_IMPLEMENTING, STATE_VERIFYING, 
        STATE_READY_TO_FINALIZE, STATE_COMPLETED, STATE_FAILED,
        get_next_action
    )
    
    sm = StateManager(req_id)
    state = sm.load()
    
    if state is None:
        return {
            "state": "NOT_FOUND",
            "req_id": req_id,
            "next_action": "call apply_req",
            "description": f"No state found for {req_id}. Call apply_req('{req_id}') first.",
        }
    
    current = state["state"]
    run_id = state.get("run_id")
    
    # State-based transitions
    if current == STATE_RUN_CREATED:
        # Move to IMPLEMENTING
        state = sm.transition(STATE_IMPLEMENTING)
        next_action = get_next_action(state)
        return {
            "state": STATE_IMPLEMENTING,
            "req_id": req_id,
            "run_id": run_id,
            "next_action": next_action["next_action"],
            "description": "Implement the requirement according to the RUN file. Call continue_req with implementation_done=True when finished.",
        }
    
    elif current == STATE_IMPLEMENTING:
        if implementation_done:
            # Move to VERIFYING
            state = sm.transition(STATE_VERIFYING)
            
            # Run verification
            errors = []
            lint_issues = lint_metadata(ROOT_DIR)
            if lint_issues > 0:
                errors.append({
                    "type": "lint",
                    "message": f"{lint_issues} lint issues found after implementation",
                    "retry_from": "continue_req",
                })
            
            req_issues = check_requirements(ROOT_DIR)
            if req_issues > 0:
                errors.append({
                    "type": "requirements",
                    "message": f"{req_issues} requirement issues found",
                    "retry_from": "continue_req",
                })
            
            if errors:
                # Back to IMPLEMENTING for fixes
                state = sm.transition(STATE_IMPLEMENTING, error={"errors": errors})
                return {
                    "state": STATE_IMPLEMENTING,
                    "req_id": req_id,
                    "run_id": run_id,
                    "errors": errors,
                    "next_action": "fix_errors",
                    "description": "Fix the errors above, then call continue_req with implementation_done=True",
                }
            
            # Verification passed
            state = sm.transition(STATE_READY_TO_FINALIZE)
            return {
                "state": STATE_READY_TO_FINALIZE,
                "req_id": req_id,
                "run_id": run_id,
                "next_action": "call finalize_run",
                "description": f"Verification passed. Call finalize_run('{run_id}') to complete.",
            }
        else:
            # Still implementing
            return {
                "state": STATE_IMPLEMENTING,
                "req_id": req_id,
                "run_id": run_id,
                "next_action": "implement",
                "description": "Continue implementation. Call continue_req with implementation_done=True when finished.",
            }
    
    elif current == STATE_VERIFYING:
        # Re-run verification
        errors = []
        lint_issues = lint_metadata(ROOT_DIR)
        if lint_issues > 0:
            errors.append({
                "type": "lint",
                "message": f"{lint_issues} lint issues found",
            })
        
        if errors:
            state = sm.transition(STATE_IMPLEMENTING, error={"errors": errors})
            return {
                "state": STATE_IMPLEMENTING,
                "req_id": req_id,
                "run_id": run_id,
                "errors": errors,
                "next_action": "fix_errors",
                "description": "Fix the errors above, then call continue_req with implementation_done=True",
            }
        
        state = sm.transition(STATE_READY_TO_FINALIZE)
        return {
            "state": STATE_READY_TO_FINALIZE,
            "req_id": req_id,
            "run_id": run_id,
            "next_action": "call finalize_run",
            "description": f"Verification passed. Call finalize_run('{run_id}') to complete.",
        }
    
    elif current == STATE_READY_TO_FINALIZE:
        return {
            "state": STATE_READY_TO_FINALIZE,
            "req_id": req_id,
            "run_id": run_id,
            "next_action": "call finalize_run",
            "description": f"Ready to finalize. Call finalize_run('{run_id}') to complete.",
        }
    
    elif current == STATE_COMPLETED:
        return {
            "state": STATE_COMPLETED,
            "req_id": req_id,
            "run_id": run_id,
            "next_action": "done",
            "description": f"{req_id} has been completed successfully.",
        }
    
    elif current == STATE_FAILED:
        next_action = get_next_action(state)
        return {
            "state": STATE_FAILED,
            "req_id": req_id,
            "run_id": run_id,
            "errors": state.get("last_error", {}).get("errors", []),
            "disc_path": state.get("disc_path"),
            "next_action": "call apply_req to retry",
            "description": "Process failed. Fix errors and call apply_req to retry.",
        }
    
    else:
        next_action = get_next_action(state)
        return {
            "state": current,
            "req_id": req_id,
            "run_id": run_id,
            "next_action": next_action.get("next_action", "unknown"),
            "description": next_action.get("description", f"Unknown state: {current}"),
        }


@mcp.tool()
def req_status(req_id: str) -> Dict[str, Any]:
    """
    Inspect REQ readiness and current state machine status.
    
    Args:
        req_id: Target REQ ID
    
    Returns:
        Combined status with REQ info and state machine state
    """
    from core.state import StateManager, get_next_action
    
    automator = Automator()
    req_info = automator.req_status(req_id)
    
    # Add state machine info
    sm = StateManager(req_id)
    state = sm.load()
    
    if state:
        next_action = get_next_action(state)
        req_info["state_machine"] = {
            "state": state["state"],
            "run_id": state.get("run_id"),
            "next_action": next_action["next_action"],
            "description": next_action["description"],
            "last_error": state.get("last_error"),
            "disc_path": state.get("disc_path"),
            "updated_at": state.get("updated_at"),
        }
    else:
        req_info["state_machine"] = {
            "state": "NOT_STARTED",
            "next_action": "call apply_req",
            "description": f"No state found. Call apply_req('{req_id}') to start processing.",
        }
    
    return req_info


@mcp.tool()
def run_report(run_id: str) -> Dict[str, Any]:
    """
    Return a structured summary of a RUN document with state info.
    
    Args:
        run_id: RUN ID
    
    Returns:
        RUN summary with state machine context
    """
    from core.state import StateManager, get_next_action
    
    automator = Automator()
    report = automator.run_report(run_id)
    
    # Extract req_id from run_id
    parts = run_id.split("-")
    if len(parts) >= 4 and parts[0] == "RUN":
        req_id = "-".join(parts[1:4])
        
        sm = StateManager(req_id)
        state = sm.load()
        
        if state:
            next_action = get_next_action(state)
            report["state_machine"] = {
                "state": state["state"],
                "next_action": next_action["next_action"],
                "description": next_action["description"],
            }
    
    return report


@mcp.tool()
def finish(run_id: str, success: Optional[bool] = True, git_hash: Optional[str] = "") -> Dict[str, Any]:
    """
    Mark a RUN as completed with evidence.

    This is the final step in the 3-Step Workflow:
    1. Intake -> Creates BRIEF
    2. Plan -> Creates RUN from BRIEF
    3. Finish (this) -> Marks RUN as completed with Git evidence

    RUN remains in active/ (no archive move per v3.4 policy).

    Args:
        run_id: RUN ID (e.g., "RUN-BRIEF-MCP-003-step-01")
        success: Whether the run succeeded
        git_hash: Git commit hash as evidence (optional)

    Returns:
        Dict with path and final state
    """
    from core.state import (
        StateManager,
        STATE_READY_TO_FINALIZE, STATE_COMPLETED, STATE_FAILED,
    )

    # Extract req_id/brief_id from run_id
    # Formats:
    #   RUN-REQ-XXX-NNN-step-NN -> REQ-XXX-NNN
    #   RUN-BRIEF-XXX-NNN-step-NN -> BRIEF-XXX-NNN
    parts = run_id.split("-")
    if len(parts) >= 4 and parts[0] == "RUN":
        if parts[1] == "REQ":
            req_id = "-".join(parts[1:4])  # REQ-XXX-NNN
        elif parts[1] == "BRIEF":
            req_id = "-".join(parts[1:4])  # BRIEF-XXX-NNN
        else:
            req_id = None
    else:
        req_id = None

    automator = Automator()

    if success:
        result_path = automator.finish(run_id, success=True, git_hash=git_hash or "")

        # Update state if we have req_id
        if req_id:
            sm = StateManager(req_id)
            state = sm.load()
            if state and state["state"] == STATE_READY_TO_FINALIZE:
                sm.transition(STATE_COMPLETED)

        return {
            "state": STATE_COMPLETED,
            "run_id": run_id,
            "req_id": req_id,
            "path": str(result_path),
            "git_hash": git_hash,
            "next_action": "done",
            "description": "Run finalized successfully. RUN stays in active/.",
        }
    else:
        # Failed finalization
        result_path = automator.finish(run_id, success=False, git_hash=git_hash or "")

        if req_id:
            sm = StateManager(req_id)
            sm.transition(
                STATE_FAILED,
                error={"errors": [{"type": "finalization", "message": "Run marked as failed"}]},
            )

        return {
            "state": STATE_FAILED,
            "run_id": run_id,
            "req_id": req_id,
            "path": str(result_path),
            "next_action": "create_disc",
            "description": "Run finalized as failed. Consider creating a discussion document.",
        }


@mcp.tool()
def finalize_run(run_id: str, success: Optional[bool] = True, git_hash: Optional[str] = "") -> Dict[str, Any]:
    """
    Alias for finish() - kept for backward compatibility.

    Args:
        run_id: RUN ID (e.g., "RUN-REQ-VALID-001-step-01")
        success: Whether the run succeeded
        git_hash: Git commit hash as evidence (optional)

    Returns:
        Dict with path and final state
    """
    return finish(run_id, success, git_hash)


@mcp.tool()
def create_disc_from_failure(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a DISC draft for a failed stage.
    
    Args:
        context: Dict with stage, errors, files, rules, logs, and req_id/target_id.
    
    Returns:
        Dict with disc_path
    """
    automator = Automator()
    disc_path = automator.create_disc_from_context(context)
    return {"disc_path": str(disc_path)}


@mcp.tool()
def validate(scope: str) -> Dict[str, Any]:
    """
    Run a single validation check and return detailed results.
    
    Args:
        scope: One of "lint", "req", "links", "structure", "doctor", "all"
    
    Returns:
        Dict with:
        - scope: Validation scope
        - issues: Number of issues found
        - passed: Boolean indicating if validation passed
        - details: List of issue details (captured from output)
        - errors: Structured error list for MCP state machine
    """
    import io
    import sys
    
    scope = scope.lower()
    issues = 0
    details = []
    
    # Capture stdout to get detailed messages
    old_stdout = sys.stdout
    sys.stdout = captured = io.StringIO()
    
    try:
        if scope == "lint":
            issues = lint_metadata(ROOT_DIR)
        elif scope == "req":
            issues = check_requirements(ROOT_DIR)
        elif scope == "links":
            issues = check_links(ROOT_DIR)
        elif scope == "structure":
            issues = check_structure(ROOT_DIR)
        elif scope == "doctor":
            issues = doctor(ROOT_DIR)
        elif scope == "all":
            # Run all checks
            issues += lint_metadata(ROOT_DIR)
            issues += check_requirements(ROOT_DIR)
            issues += check_links(ROOT_DIR)
            issues += check_structure(ROOT_DIR)
        else:
            sys.stdout = old_stdout
            raise ValueError(f"Unknown scope: {scope}. Use: lint, req, links, structure, doctor, all")
    finally:
        sys.stdout = old_stdout
    
    # Parse captured output for details
    output = captured.getvalue()
    for line in output.splitlines():
        line = line.strip()
        if line and (line.startswith("!") or line.startswith("Missing") or "issue" in line.lower()):
            details.append(line)
    
    # Build structured errors for state machine
    errors = []
    if issues > 0:
        for detail in details:
            if detail.startswith("!"):
                errors.append({
                    "type": scope,
                    "message": detail[1:].strip(),
                    "retry_from": "validate",
                })
    
    return {
        "scope": scope,
        "issues": issues,
        "passed": issues == 0,
        "details": details,
        "errors": errors,
        "next_action": "none" if issues == 0 else "fix_errors",
        "description": "All validations passed" if issues == 0 else f"Found {issues} issue(s). Fix and re-run validation.",
    }


# Legacy alias for backward compatibility
apply_req_tool = apply_req


def _call_with_optional(func, **kwargs):
    try:
        sig = inspect.signature(func)
    except (TypeError, ValueError):
        return func()
    params = {k: v for k, v in kwargs.items() if k in sig.parameters}
    return func(**params)


def run_server(mode: str = "stdio", host: str = "127.0.0.1", port: int = 8765) -> None:
    if mode == "http":
        if hasattr(mcp, "run_http_async"):
            asyncio.run(mcp.run_http_async(host=host, port=port))
            return
        if hasattr(mcp, "run_async"):
            asyncio.run(mcp.run_async(transport="http", host=host, port=port))
            return
        if hasattr(mcp, "run"):
            _call_with_optional(mcp.run, transport="http", host=host, port=port)
            return
        raise RuntimeError("HTTP mode not supported by installed MCP runtime.")
    if hasattr(mcp, "run_stdio_async"):
        asyncio.run(mcp.run_stdio_async())
        return
    if hasattr(mcp, "run_async"):
        asyncio.run(mcp.run_async(transport="stdio"))
        return
    if hasattr(mcp, "run"):
        _call_with_optional(mcp.run, transport="stdio")
        return
    raise RuntimeError("STDIO mode not supported by installed MCP runtime.")


def main() -> int:
    parser = argparse.ArgumentParser(description="MemoryAtlas MCP Server")
    parser.add_argument("--stdio", action="store_true", help="Run in STDIO mode")
    parser.add_argument("--http", action="store_true", help="Run in HTTP mode")
    parser.add_argument("--host", default="127.0.0.1", help="HTTP host")
    parser.add_argument("--port", type=int, default=8765, help="HTTP port")
    args = parser.parse_args()
    mode = "http" if args.http else "stdio"
    run_server(mode=mode, host=args.host, port=args.port)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
