from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

from core.config import CURRENT_VERSION, MCP_DEFINITIONS, ROOT_DIR
from utils.fs import update_mcp_definitions, write_file

VALID_TARGETS = {"claude_code", "claude_desktop", "codex", "gemini_cli", "ci"}
VALID_OS = {"windows", "unix"}


def _python_path(os_name: str) -> str:
    if os_name == "windows":
        return ".venv-mcp\\Scripts\\python.exe"
    return ".venv-mcp/bin/python"


def _render_mcp_template(os_name: str) -> str:
    payload = {
        "mcpServers": {
            "memoryatlas": {
                "command": _python_path(os_name),
                "args": [".memory/00_SYSTEM/mcp/mcp_server.py", "--stdio"],
                "env": {},
            }
        }
    }
    return json.dumps(payload, indent=2)


def _render_prompt(target: str, os_name: str) -> str:
    lines: List[str] = [
        "# MCP Bootstrap Prompt",
        "",
        "Goal: Configure MCP so the client can auto-spawn the MemoryAtlas server on demand.",
        f"Target client: {target}",
        f"OS: {os_name}",
        "Python strategy: default to .venv-mcp unless specified otherwise.",
        "",
        "Constraints:",
        "- Do NOT edit anything under 02_REQUIREMENTS automatically.",
        "- Use STDIO mode for MCP server execution.",
        "",
        "Project context:",
        "- Repo root contains .memory/ and memory_manager.py",
        "- MCP entrypoint: .memory/00_SYSTEM/mcp/mcp_server.py",
        "",
        "MCP tool definitions:",
    ]
    for name, spec in sorted(MCP_DEFINITIONS.items()):
        lines.append(f"- {spec['signature']}: {spec['summary']}")
    lines.extend(
        [
            "",
            "Required outputs (fixed format):",
            "1) List of files to create or update (with paths).",
            "2) Full contents of each file or a unified diff patch.",
            "3) Installation / connection steps (3-5 steps).",
            "4) Verification steps (commands to run).",
            "",
            "Must include:",
            "- apply_req_full two-call flow in MCP README.",
            "- Requires-Spec metadata example in MCP README.",
            "- create_disc_from_failure(context) example in MCP README.",
            "",
            "Default file targets:",
            f"- .memory/00_SYSTEM/mcp/templates/{target}.mcp.json",
            "- .memory/00_SYSTEM/scripts/run_mcp_server.ps1",
            "- .memory/00_SYSTEM/scripts/run_mcp_server.sh",
            "",
            "Validation commands:",
            "- python memory_manager.py --doctor",
            f"- python memory_manager.py --mcp-check --target {target}",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def _render_checklist(target: str, os_name: str) -> str:
    return (
        "# MCP Bootstrap Checklist\n\n"
        f"- [ ] Target: {target}\n"
        f"- [ ] OS: {os_name}\n"
        "- [ ] MCP README updated (auto-generated)\n"
        f"- [ ] Template created: .memory/00_SYSTEM/mcp/templates/{target}.mcp.json\n"
        "- [ ] Script created: .memory/00_SYSTEM/scripts/run_mcp_server.ps1\n"
        "- [ ] Script created: .memory/00_SYSTEM/scripts/run_mcp_server.sh\n"
        "- [ ] Client config applied from template\n"
        "- [ ] `python memory_manager.py --doctor` passes\n"
        f"- [ ] `python memory_manager.py --mcp-check --target {target}` passes\n"
    )


def _render_run_script_ps1() -> str:
    return (
        "$ErrorActionPreference = \"Stop\"\n"
        "$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path\n"
        "$systemDir = Split-Path -Parent $scriptDir\n"
        "$memoryDir = Split-Path -Parent $systemDir\n"
        "$repoDir = Split-Path -Parent $memoryDir\n"
        "$python = Join-Path $repoDir \".venv-mcp\\\\Scripts\\\\python.exe\"\n"
        "$server = Join-Path $memoryDir \"00_SYSTEM\\\\mcp\\\\mcp_server.py\"\n"
        "& $python $server --stdio\n"
    )


def _render_run_script_sh() -> str:
    return (
        "#!/usr/bin/env bash\n"
        "set -euo pipefail\n"
        "script_dir=\"$(cd \"$(dirname \"${BASH_SOURCE[0]}\")\" && pwd)\"\n"
        "system_dir=\"$(cd \"$script_dir/..\" && pwd)\"\n"
        "memory_dir=\"$(cd \"$system_dir/..\" && pwd)\"\n"
        "repo_dir=\"$(cd \"$memory_dir/..\" && pwd)\"\n"
        "python=\"$repo_dir/.venv-mcp/bin/python\"\n"
        "\"$python\" \"$memory_dir/00_SYSTEM/mcp/mcp_server.py\" --stdio\n"
    )


def bootstrap_mcp(target: str, os_name: str, dry_run: bool = False) -> None:
    if target not in VALID_TARGETS:
        raise ValueError(f"Unknown target: {target}. Use: {', '.join(sorted(VALID_TARGETS))}")
    if os_name not in VALID_OS:
        raise ValueError(f"Unknown OS: {os_name}. Use: windows or unix")

    root = Path(ROOT_DIR)
    mcp_dir = root / "00_SYSTEM" / "mcp"
    templates_dir = mcp_dir / "templates"
    scripts_dir = root / "00_SYSTEM" / "scripts"
    mcp_dir.mkdir(parents=True, exist_ok=True)
    templates_dir.mkdir(parents=True, exist_ok=True)
    scripts_dir.mkdir(parents=True, exist_ok=True)

    update_mcp_definitions(ROOT_DIR, dry_run=dry_run)

    prompt_path = mcp_dir / f"BOOTSTRAP_MCP_PROMPT_{target}_{os_name}.md"
    checklist_path = mcp_dir / f"BOOTSTRAP_MCP_CHECKLIST_{target}_{os_name}.md"
    template_path = templates_dir / f"{target}.mcp.json"
    script_ps1 = scripts_dir / "run_mcp_server.ps1"
    script_sh = scripts_dir / "run_mcp_server.sh"

    files: Dict[Path, str] = {
        prompt_path: _render_prompt(target, os_name),
        checklist_path: _render_checklist(target, os_name),
        template_path: _render_mcp_template(os_name),
        script_ps1: _render_run_script_ps1(),
        script_sh: _render_run_script_sh(),
    }

    print("\n" + "=" * 60)
    print("MCP Bootstrap")
    print("=" * 60)
    for path, content in files.items():
        rel = path.as_posix()
        if dry_run:
            print(f"  [DRY-RUN] Would write: {rel}")
            continue
        write_file(str(path), content)
        print(f"  [WRITE] {rel}")

    print("\nNext steps:")
    print(f"  1) Apply the template: {template_path.as_posix()}")
    print("  2) Configure your client to auto-spawn the MCP server (STDIO).")
    print("  3) Validate with --doctor and --mcp-check.")
