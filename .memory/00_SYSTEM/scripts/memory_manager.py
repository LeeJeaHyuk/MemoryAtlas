
import json
import os
import re
import shutil
from datetime import datetime
from typing import List, Optional

from core.config import (
    CURRENT_VERSION,
    DIRS,
    DOC_TEMPLATES,
    MCP_DEFINITIONS,
    SYSTEM_TEMPLATES,
    TEMPLATE_VERSION,
    UPDATABLE_READMES,
)

ONBOARDING_GUIDE_PATH = "GETTING_STARTED.md"
ONBOARDING_PROMPT_REL_PATH = "00_SYSTEM/ONBOARDING_PROMPT.md"
ONBOARDING_STATE_REL_PATH = "00_SYSTEM/state/onboarding.json"
ONBOARDING_NOTE_PLACEHOLDERS = {"(자유롭게 기록)", "(작성 내용 없음)"}
ONBOARDING_NOTES_RE = re.compile(
    r"<!-- NOTES:BEGIN -->(.*?)<!-- NOTES:END -->", re.S
)
ONBOARDING_ID_RE = re.compile(r"<!-- id:([a-z0-9_.-]+) -->")
ONBOARDING_CHECKBOX_RE = re.compile(
    r"^(\s*- \[)(?P<mark>[ xX])(\] .+?<!-- id:(?P<id>[^ ]+) -->\s*)$",
    re.M,
)

def write_file(path: str, content: str, dry_run: bool = False) -> None:
    """Write content to file, creating parent directories if needed."""
    if dry_run:
        return
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def read_text(path: str) -> str:
    """Read text from file with error handling."""
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def safe_move(src: str, dest: str, dry_run: bool = False) -> bool:
    """Safely move file/directory."""
    if not os.path.exists(src):
        return False
    if dry_run:
        return True
    dest_dir = os.path.dirname(dest)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)
    if os.path.exists(dest):
        return False
    try:
        shutil.move(src, dest)
        return True
    except Exception as e:
        print(f"  ! Failed to move {src}: {e}")
        return False

def ensure_structure(root: str) -> None:
    """Ensure all required directories exist."""
    for folder in DIRS:
        os.makedirs(os.path.join(root, folder), exist_ok=True)

def _current_date() -> str:
    return datetime.now().strftime("%Y-%m-%d")

def _extract_onboarding_ids(template: str) -> list[str]:
    ids = ONBOARDING_ID_RE.findall(template)
    return sorted(set(ids))

def _normalize_notes(notes: str) -> str:
    trimmed = notes.strip()
    if not trimmed or trimmed in ONBOARDING_NOTE_PLACEHOLDERS:
        return ""
    return notes.strip("\n").rstrip()

def _extract_notes(text: str) -> Optional[str]:
    match = ONBOARDING_NOTES_RE.search(text)
    if not match:
        return None
    return match.group(1).strip("\n")

def load_onboarding_state(root: str, template: str) -> tuple[dict, bool, bool]:
    """Load onboarding state and normalize missing fields."""
    state_path = os.path.join(root, *ONBOARDING_STATE_REL_PATH.split("/"))
    state_exists = os.path.exists(state_path)
    state_changed = False

    state: dict = {}
    if state_exists:
        try:
            with open(state_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    state = data
        except Exception:
            state = {}

    if "schema_version" not in state:
        state["schema_version"] = 1
        state_changed = True
    if state.get("template_version") != TEMPLATE_VERSION:
        state["template_version"] = TEMPLATE_VERSION
        state_changed = True
    if not isinstance(state.get("items"), dict):
        state["items"] = {}
        state_changed = True
    if not isinstance(state.get("notes"), str):
        state["notes"] = ""
        state_changed = True
    if not isinstance(state.get("last_updated"), str):
        state["last_updated"] = "(TBD)"
        state_changed = True

    for item_id in _extract_onboarding_ids(template):
        if item_id not in state["items"]:
            state["items"][item_id] = False
            state_changed = True

    return state, state_changed, state_exists

def sync_onboarding_state_from_guide(guide_text: str, state: dict) -> bool:
    """Sync checkbox state and notes from existing guide content."""
    changed = False
    for match in ONBOARDING_CHECKBOX_RE.finditer(guide_text):
        item_id = match.group("id")
        done = match.group("mark").lower() == "x"
        current = state["items"].get(item_id)
        if current is None or current != done:
            state["items"][item_id] = done
            changed = True

    notes = _extract_notes(guide_text)
    if notes is not None:
        normalized = _normalize_notes(notes)
        if normalized != state.get("notes", ""):
            state["notes"] = normalized
            changed = True

    return changed

def _compute_onboarding_status(items: dict) -> str:
    if not items:
        return "Not Started"
    total = len(items)
    done = sum(1 for value in items.values() if value)
    if done == 0:
        return "Not Started"
    if done == total:
        return "Completed"
    return "In Progress"

def render_onboarding_guide(template: str, state: dict) -> str:
    """Render the onboarding guide template with current state."""
    def replace_checkbox(match: re.Match) -> str:
        item_id = match.group("id")
        done = state.get("items", {}).get(item_id, False)
        mark = "x" if done else " "
        return f"{match.group(1)}{mark}{match.group(3)}"

    rendered = ONBOARDING_CHECKBOX_RE.sub(replace_checkbox, template)
    status = _compute_onboarding_status(state.get("items", {}))
    last_updated = state.get("last_updated") or "(TBD)"
    rendered = rendered.replace("{STATUS}", status)
    rendered = rendered.replace("{LAST_UPDATED}", last_updated)

    notes = state.get("notes", "")
    notes_body = _normalize_notes(notes)
    if not notes_body:
        notes_body = "(자유롭게 기록)"
    rendered = ONBOARDING_NOTES_RE.sub(
        f"<!-- NOTES:BEGIN -->\n{notes_body}\n<!-- NOTES:END -->",
        rendered,
    )
    return rendered

def update_onboarding_guide(root: str, dry_run: bool = False, force: bool = False) -> None:
    """Update onboarding guide using template + state."""
    template = DOC_TEMPLATES.get(ONBOARDING_GUIDE_PATH)
    if not template:
        return

    state, state_changed, state_exists = load_onboarding_state(root, template)

    guide_path = os.path.join(root, ONBOARDING_GUIDE_PATH)
    if os.path.exists(guide_path):
        guide_text = read_text(guide_path)
        if sync_onboarding_state_from_guide(guide_text, state):
            state_changed = True

    if state_changed or not state_exists or force:
        state["last_updated"] = _current_date()

    if dry_run:
        print(f"  - Would update onboarding guide: {ONBOARDING_GUIDE_PATH}")
        if state_changed or not state_exists or force:
            print(f"  - Would update onboarding state: {ONBOARDING_STATE_REL_PATH}")
        return

    if state_changed or not state_exists or force:
        state_path = os.path.join(root, *ONBOARDING_STATE_REL_PATH.split("/"))
        write_file(state_path, json.dumps(state, indent=2, sort_keys=True) + "\n")

    rendered = render_onboarding_guide(template, state)
    write_file(guide_path, rendered)
    print(f"  * Updated onboarding guide: {ONBOARDING_GUIDE_PATH}")

def update_onboarding_prompt(root: str, dry_run: bool = False) -> None:
    """Update onboarding prompt in 00_SYSTEM for manual refresh."""
    content = DOC_TEMPLATES.get(ONBOARDING_PROMPT_REL_PATH)
    if not content:
        return
    if dry_run:
        print(f"  - Would update onboarding prompt: {ONBOARDING_PROMPT_REL_PATH}")
        return
    prompt_path = os.path.join(root, *ONBOARDING_PROMPT_REL_PATH.split("/"))
    write_file(prompt_path, content)
    print(f"  * Updated onboarding prompt: {ONBOARDING_PROMPT_REL_PATH}")

def create_missing_docs(root: str, dry_run: bool = False) -> None:
    """Create missing template documents."""
    for rel_path, content in DOC_TEMPLATES.items():
        if rel_path == ONBOARDING_GUIDE_PATH:
            continue
        path = os.path.join(root, rel_path)
        if os.path.exists(path):
            continue
        if dry_run:
            print(f"  - Would create doc: {rel_path}")
            continue
        dir_name = os.path.dirname(path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        write_file(path, content)
        print(f"  + Created doc: {rel_path}")

def update_system_templates(root: str, dry_run: bool = False) -> None:
    """Update system-managed template files."""
    for rel_path, content in SYSTEM_TEMPLATES.items():
        path = os.path.join(root, rel_path)
        if dry_run:
            print(f"  - Would update system file: {rel_path}")
            continue
        dir_name = os.path.dirname(path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        write_file(path, content)
        print(f"  * Updated system file: {rel_path}")


def update_readme_files(root: str, dry_run: bool = False) -> None:
    """Update README files that are system-managed."""
    for rel_path in UPDATABLE_READMES:
        if rel_path not in DOC_TEMPLATES:
            continue
        path = os.path.join(root, rel_path)
        content = DOC_TEMPLATES[rel_path]
        if dry_run:
            print(f"  - Would update readme: {rel_path}")
            continue
        dir_name = os.path.dirname(path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        write_file(path, content)
        print(f"  * Updated readme: {rel_path}")

def render_mcp_collection(definitions: dict) -> str:
    """Render single MCP documentation file that covers all definitions."""
    lines = [
        "# MCP Definitions",
        "",
        "System-generated. Do not edit directly.",
        "",
        "Each section below documents an MCP function exposed by MemoryAtlas.",
        "",
    ]
    for name, spec in sorted(definitions.items()):
        lines.extend(
            [
                f"## {name}",
                "",
                "### Signature",
                f"`{spec['signature']}`",
                "",
                "### Summary",
                spec["summary"],
                "",
                "### Inputs",
            ]
        )
        inputs = spec.get("inputs", [])
        if inputs:
            lines.extend(f"- {item}" for item in inputs)
        else:
            lines.append("- (none)")
        lines.extend(["", "### Outputs"])
        outputs = spec.get("outputs", [])
        if outputs:
            lines.extend(f"- {item}" for item in outputs)
        else:
            lines.append("- (none)")
        behavior = spec.get("behavior", [])
        if behavior:
            lines.extend(["", "### Behavior"])
            lines.extend(f"- {item}" for item in behavior)
        lines.append("")  # blank line between sections
    lines.extend(render_mcp_connection_guide())
    return "\n".join(lines).rstrip() + "\n"


def render_mcp_connection_guide() -> List[str]:
    """Render connection guide and templates overview."""
    return [
        "## Connection Guide",
        "",
        "### Entry Points",
        "- STDIO: `python .memory/00_SYSTEM/mcp/mcp_server.py --stdio`",
        "- HTTP: `python .memory/00_SYSTEM/mcp/mcp_server.py --http --host 127.0.0.1 --port 8765`",
        "- Module: `python -m memoryatlas_mcp --stdio`",
        "",
        "### Auto-Launch Behavior",
        "- STDIO clients can auto-spawn the server process on demand using the configured command.",
        "- This means the server does not need to be manually running in the background.",
        "- HTTP mode still requires a long-running server process.",
        "",
        "### One-Shot Flow (apply_req_full)",
        "- Call `apply_req_full(req_id)` to create the RUN and receive instructions.",
        "- Implement changes, then call `apply_req_full(req_id)` again to verify and finalize.",
        "",
        "### Spec Auto-Trigger",
        "- Set REQ metadata `> **Requires-Spec**: true` to auto-create 03 specs.",
        "",
        "### DISC Context Example",
        "- `create_disc_from_failure({\"req_id\":\"REQ-MCP-001\",\"stage\":\"validate\",\"errors\":[{\"type\":\"links\",\"message\":\"3 link issues\"}],\"files\":[\"02_REQUIREMENTS/README.md\"],\"rules\":[\"RULE-LINK-001\"],\"logs\":\"...\"})`",
        "",
        "### Client Config Templates",
        "- `claude_code.mcp.json` (STDIO)",
        "- `codex.mcp.json` (STDIO)",
        "- `gemini_cli.mcp.json` (STDIO)",
        "- Bootstrap templates: `00_SYSTEM/mcp/templates/<target>.mcp.json` (from --bootstrap-mcp)",
        "",
        "### Notes",
        "- Clients usually require one-time server registration.",
        "- HTTP mode may require authentication and is optional.",
        "",
    ]


def update_mcp_definitions(root: str, dry_run: bool = False) -> None:
    """Generate MCP definition documentation under 00_SYSTEM/mcp/."""
    dir_path = os.path.join(root, "00_SYSTEM", "mcp")
    os.makedirs(dir_path, exist_ok=True)
    rel_path = os.path.join("00_SYSTEM", "mcp", "README.md")
    path = os.path.join(root, rel_path)
    content = render_mcp_collection(MCP_DEFINITIONS)
    if dry_run:
        print(f"  - Would update mcp: {rel_path}")
        return
    write_file(path, content)
    print(f"  * Updated mcp: {rel_path}")
    update_mcp_server_entrypoint(root, dry_run=dry_run)
    update_mcp_client_templates(root, dry_run=dry_run)


def update_mcp_server_entrypoint(root: str, dry_run: bool = False) -> None:
    """Write MCP server entrypoint under 00_SYSTEM/mcp/."""
    rel_path = os.path.join("00_SYSTEM", "mcp", "mcp_server.py")
    path = os.path.join(root, rel_path)
    content = render_mcp_server_entrypoint()
    if dry_run:
        print(f"  - Would update mcp: {rel_path}")
        return
    write_file(path, content)
    print(f"  * Updated mcp: {rel_path}")


def render_mcp_server_entrypoint() -> str:
    return (
        "#!/usr/bin/env python3\n"
        "from __future__ import annotations\n"
        "import argparse\n"
        "import sys\n"
        "from pathlib import Path\n"
        "\n"
        "ROOT = Path(__file__).resolve().parents[3]\n"
        "SRC = ROOT / \"src\"\n"
        "sys.path.insert(0, str(SRC))\n"
        "\n"
        "try:\n"
        "    from mcp_server import run_server\n"
        "except Exception as exc:\n"
        "    print(f\"Failed to import MCP server: {exc}\")\n"
        "    sys.exit(1)\n"
        "\n"
        "def main() -> int:\n"
        "    parser = argparse.ArgumentParser(description=\"MemoryAtlas MCP Server\")\n"
        "    parser.add_argument(\"--stdio\", action=\"store_true\", help=\"Run in STDIO mode\")\n"
        "    parser.add_argument(\"--http\", action=\"store_true\", help=\"Run in HTTP mode\")\n"
        "    parser.add_argument(\"--host\", default=\"127.0.0.1\", help=\"HTTP host\")\n"
        "    parser.add_argument(\"--port\", type=int, default=8765, help=\"HTTP port\")\n"
        "    args = parser.parse_args()\n"
        "    mode = \"http\" if args.http else \"stdio\"\n"
        "    run_server(mode=mode, host=args.host, port=args.port)\n"
        "    return 0\n"
        "\n"
        "if __name__ == \"__main__\":\n"
        "    raise SystemExit(main())\n"
    )


def update_mcp_client_templates(root: str, dry_run: bool = False) -> None:
    """Write MCP client config templates."""
    templates = {
        "claude_code.mcp.json": render_mcp_template_stdio("memoryatlas"),
        "codex.mcp.json": render_mcp_template_stdio("memoryatlas"),
        "gemini_cli.mcp.json": render_mcp_template_stdio("memoryatlas"),
    }
    for name, content in templates.items():
        rel_path = os.path.join("00_SYSTEM", "mcp", name)
        path = os.path.join(root, rel_path)
        if dry_run:
            print(f"  - Would update mcp: {rel_path}")
            continue
        write_file(path, content)
        print(f"  * Updated mcp: {rel_path}")


def render_mcp_template_stdio(server_name: str) -> str:
    return (
        "{\n"
        f"  \"mcpServers\": {{\n"
        f"    \"{server_name}\": {{\n"
        "      \"command\": \"python\",\n"
        "      \"args\": [\".memory/00_SYSTEM/mcp/mcp_server.py\", \"--stdio\"],\n"
        "      \"env\": {}\n"
        "    }\n"
        "  }\n"
        "}\n"
    )

def update_tooling(root: str, dry_run: bool = False) -> None:
    """Copy current script to system scripts directory."""
    src = os.path.abspath(__file__)
    dest = os.path.join(root, "00_SYSTEM", "scripts", "memory_manager.py")
    dest_dir = os.path.dirname(dest)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)
    if os.path.abspath(src) != os.path.abspath(dest):
        if dry_run:
            print(f"  - Would update tool: {dest}")
            return
        shutil.copyfile(src, dest)
        print(f"  * Updated tool: 00_SYSTEM/scripts/memory_manager.py")

def read_version(root: str) -> str:
    """Read installed version from VERSION file."""
    version_file = os.path.join(root, "VERSION")
    if not os.path.exists(version_file):
        return "0.0.0"
    with open(version_file, "r", encoding="utf-8") as f:
        return f.read().strip()

def write_version(root: str, dry_run: bool = False) -> None:
    """Write current version to VERSION file."""
    version_file = os.path.join(root, "VERSION")
    if dry_run:
        print(f"  - Would update version to: {CURRENT_VERSION}")
        return
    write_file(version_file, CURRENT_VERSION)
