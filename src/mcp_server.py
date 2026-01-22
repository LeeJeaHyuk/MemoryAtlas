import argparse
import inspect
from typing import Any, Dict, Optional

try:
    from fastmcp import MCP
except ImportError:  # pragma: no cover
    class MCP:
        def tool(self):
            def decorator(func):
                return func
            return decorator

mcp = MCP()

from core.automation import Automator
from core.checks import check_links, check_requirements, check_structure, doctor, lint_metadata
from core.config import ROOT_DIR


@mcp.tool()
def apply_req(
    req_id: str,
    dry_run: Optional[bool] = False,
    create_spec: Optional[bool] = True,
) -> Dict[str, Any]:
    """
    Orchestrate the REQ -> RUN pipeline with validation gates.
    
    Args:
        req_id: Target REQ ID (e.g., "REQ-VALID-001")
        dry_run: Preview only, no actual changes
    
    Returns:
        Report with status, artifacts, errors, and disc path on failure
    """
    automator = Automator()
    if not automator.validate_req(req_id):
        raise ValueError(f"REQ validation failed: {automator.last_error}")
    return automator.apply_req(req_id, dry_run=dry_run, create_spec=bool(create_spec))


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
    return {"run_path": str(run_path)}


@mcp.tool()
def req_status(req_id: str) -> Dict[str, Any]:
    """Inspect REQ readiness without executing pipeline."""
    automator = Automator()
    return automator.req_status(req_id)


@mcp.tool()
def run_report(run_id: str) -> Dict[str, Any]:
    """Return a structured summary of a RUN document."""
    automator = Automator()
    return automator.run_report(run_id)


@mcp.tool()
def finalize_run(run_id: str, success: Optional[bool] = True) -> Dict[str, Any]:
    """
    Mark a RUN as completed and archive it.
    
    Args:
        run_id: RUN ID (e.g., "RUN-REQ-VALID-001-step-01")
        success: Whether the run succeeded
    
    Returns:
        Dict with archived_path
    """
    automator = Automator()
    archived_path = automator.finalize_run(run_id, success=success)
    return {"archived_path": str(archived_path)}


@mcp.tool()
def create_disc_from_failure(target_id: str, error_log: str) -> Dict[str, Any]:
    """
    Generate a DISC draft for a failed stage.
    
    Args:
        target_id: Related REQ/RULE ID
        error_log: Error details to include
    
    Returns:
        Dict with disc_path
    """
    automator = Automator()
    disc_path = automator.create_disc_from_failure(target_id, error_log)
    return {"disc_path": str(disc_path)}


@mcp.tool()
def validate(scope: str) -> Dict[str, Any]:
    """
    Run a single validation check and return issue count.
    
    Args:
        scope: One of "lint", "req", "links", "structure", "doctor"
    
    Returns:
        Dict with scope, issues count, and passed boolean
    """
    scope = scope.lower()
    issues = 0
    
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
    else:
        raise ValueError(f"Unknown scope: {scope}. Use: lint, req, links, structure, doctor")
    
    return {
        "scope": scope,
        "issues": issues,
        "passed": issues == 0
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
        for name in ("run_http", "serve_http", "run", "serve"):
            handler = getattr(mcp, name, None)
            if handler:
                _call_with_optional(handler, host=host, port=port)
                return
        raise RuntimeError("HTTP mode not supported by installed MCP runtime.")
    for name in ("run_stdio", "run", "serve"):
        handler = getattr(mcp, name, None)
        if handler:
            _call_with_optional(handler)
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
