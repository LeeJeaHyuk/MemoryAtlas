#!/usr/bin/env python3
"""Atlas vNext CLI."""

import argparse
import json
import os
import re
import sys
import subprocess
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterable, Optional

ATLAS_VERSION = "0.3.0"

CHANGELOG = {
    "0.3.0": [
        "Refactor: SSOT-first structure (views/adr/drafts/inbox/archive).",
        "Feature: capture/run workflow with REQ-based RUN IDs.",
        "Feature: finish writes Implemented-Git/Linked-RUN to REQ.",
        "Feature: doctor validates view refs and git evidence.",
        "Templates: add VIEW/ADR; update RUN/REQ."
    ],
    "0.2.0": [
        "Feature: Auto-detection of version updates.",
        "Feature: Print changelog on update.",
    ],
    "0.1.0": [
        "Initial release."
    ]
}

# If running from src/atlas_cli.py, parents[1] is the root.
# If bundled as atlas.py in the root, parents[0] (or .parent) is the root.
_path = Path(__file__).resolve()
if _path.name == "atlas_cli.py":
    REPO_ROOT = _path.parents[1]
else:
    REPO_ROOT = _path.parent

ATLAS_ROOT = REPO_ROOT / ".atlas"
SYSTEM_ROOT = ATLAS_ROOT / ".system"
TEMPLATES_DIR = SYSTEM_ROOT / "templates"
STATE_DIR = SYSTEM_ROOT / "state"
LAST_RUN_PATH = STATE_DIR / "last_run.json"
VERSION_PATH = SYSTEM_ROOT / "VERSION"
SRC_DEFAULTS_ROOT = REPO_ROOT / "src" / ".system_defaults"
SRC_DEFAULT_TEMPLATES_DIR = SRC_DEFAULTS_ROOT / "templates"
SRC_DEFAULT_TOP_DOCS_DIR = SRC_DEFAULTS_ROOT / "top_docs"
SRC_DEFAULT_PROMPTS_DIR = SRC_DEFAULTS_ROOT / "prompts"
SRC_DEFAULT_DIR_READMES_DIR = SRC_DEFAULTS_ROOT / "dir_readmes"

REQ_DIR = ATLAS_ROOT / "req"
RULE_DIR = ATLAS_ROOT / "rule"
ADR_DIR = ATLAS_ROOT / "adr"
CQ_DIR = ATLAS_ROOT / "cq"
VIEWS_DIR = ATLAS_ROOT / "views"
INBOX_DIR = ATLAS_ROOT / "inbox"  # Unstructured notes, excluded from doctor
DRAFTS_DIR = ATLAS_ROOT / "drafts"
BRIEF_DIR = DRAFTS_DIR / "brief"
RUN_DIR = ATLAS_ROOT / "runs"
ARCHIVE_DIR = ATLAS_ROOT / "archive"

REQUIRED_TOP_DOCS = [
    ATLAS_ROOT / "FRONT.md",
    ATLAS_ROOT / "BOARD.md",
    ATLAS_ROOT / "CONVENTIONS.md",
]

OPTIONAL_TOP_DOCS = [
    ATLAS_ROOT / "GOALS.md",
]

REQ_ID_PATTERN = re.compile(r"^REQ-([A-Z]+)-(\d{3})$")
RULE_ID_PATTERN = re.compile(r"^RULE-([A-Z]+)-(\d{3})$")
ADR_ID_PATTERN = re.compile(r"^ADR-([A-Z]+)-(\d{3})$")
CQ_ID_PATTERN = re.compile(r"^CQ-([A-Z]+)-(\d{3})$")
BRIEF_ID_PATTERN = re.compile(r"^BRIEF-([A-Z]+)-(\d{3})$")
RUN_ID_PATTERN = re.compile(r"^RUN-(BRIEF|REQ)-([A-Z]+)-(\d{3})-step-(\d{2})$")

META_RE = re.compile(r"^>\s*\*\*([^*]+)\*\*:\s*(.+)$")
HEADER_ID_RE = re.compile(r"^#\s+\[([^\]]+)\]", re.M)
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
SSOT_ID_RE = re.compile(r"(?:REQ|RULE|ADR)-[A-Z]+-\d{3}")
REF_TOKEN_RE = re.compile(r"@(?P<id>(?:REQ|RULE|ADR)-[A-Z]+-\d{3})(?:#[^)\s]+)?")
NORMATIVE_KEYWORDS = ["반드시", "해야", "불가", "금지", "항상", "MUST", "SHOULD", "MAY"]

ALLOWED_MUST_READ_PREFIXES = {"RULE"}

PATCH_DIR = ATLAS_ROOT / "patch"

# Embedded source code (populated by build.py)
# __EMBEDDED_SRC_PLACEHOLDER__ will be replaced with base64-encoded source
EMBEDDED_SRC_B64 = "__EMBEDDED_SRC_PLACEHOLDER__"
# Embedded defaults bundle (populated by build.py)
# __EMBEDDED_DEFAULTS_PLACEHOLDER__ will be replaced with base64-encoded JSON
EMBEDDED_DEFAULTS_B64 = "__EMBEDDED_DEFAULTS_PLACEHOLDER__"
_EMBEDDED_DEFAULTS_CACHE: Optional[dict[str, str]] = None

# Checkbox patterns
CHECKBOX_UNCHECKED = re.compile(r"^(\s*)-\s*\[\s*\](.*)$")
CHECKBOX_CHECKED = re.compile(r"^(\s*)-\s*\[x\](.*)$", re.IGNORECASE)
TRACEABILITY_LINK_RE = re.compile(r"\*\*(?:Implements|Answers|Solved by|Implemented by)\*\*:\s*\[([^\]]+)\]\(([^)]+)\)")

TOP_DOC_FILENAMES = ["FRONT.md", "BOARD.md", "CONVENTIONS.md", "GOALS.md"]
TEMPLATE_NAMES = ["REQ.md", "RULE.md", "CQ.md", "BRIEF.md", "RUN.md", "VIEW.md", "ADR.md"]
PROMPT_NAMES = ["onboarding.md"]
DIR_README_PATHS = [
    Path("req/README.md"),
    Path("views/README.md"),
    Path("runs/README.md"),
    Path("rule/README.md"),
    Path("adr/README.md"),
    Path("cq/README.md"),
    Path("drafts/brief/README.md"),
]






def get_version() -> str:
    """Read version from VERSION file (SSOT)."""
    if VERSION_PATH.exists():
        return VERSION_PATH.read_text(encoding="utf-8").strip()
    return "unknown"


def now_date() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def backup_file(path: Path) -> Optional[Path]:
    """Backup file to ARCHIVE_DIR with timestamp."""
    if not path.exists():
        return None
    
    ensure_dir(ARCHIVE_DIR)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    safe_name = f"{path.parent.name}_{path.name}"
    backup_name = f"{timestamp}_{safe_name}"
    backup_path = ARCHIVE_DIR / backup_name
    
    try:
        shutil.copy2(path, backup_path)
        return backup_path
    except Exception as e:
        print(f"[WARN] Failed to backup {path}: {e}")
        return None


def load_embedded_defaults() -> dict[str, str]:
    """Decode embedded defaults bundle if present."""
    global _EMBEDDED_DEFAULTS_CACHE
    if _EMBEDDED_DEFAULTS_CACHE is not None:
        return _EMBEDDED_DEFAULTS_CACHE
    if EMBEDDED_DEFAULTS_B64 == "__EMBEDDED_DEFAULTS_PLACEHOLDER__":
        _EMBEDDED_DEFAULTS_CACHE = {}
        return _EMBEDDED_DEFAULTS_CACHE
    try:
        import base64

        decoded = base64.b64decode(EMBEDDED_DEFAULTS_B64).decode("utf-8")
        data = json.loads(decoded)
        if isinstance(data, dict):
            _EMBEDDED_DEFAULTS_CACHE = {str(k): str(v) for k, v in data.items()}
            return _EMBEDDED_DEFAULTS_CACHE
    except Exception:
        pass
    _EMBEDDED_DEFAULTS_CACHE = {}
    return _EMBEDDED_DEFAULTS_CACHE


def load_default_top_docs() -> dict[Path, str]:
    embedded = load_embedded_defaults()
    if not SRC_DEFAULT_TOP_DOCS_DIR.is_dir():
        docs: dict[Path, str] = {}
        missing: list[str] = []
        for name in TOP_DOC_FILENAMES:
            key = f"top_docs/{name}"
            if key not in embedded:
                missing.append(name)
                continue
            docs[ATLAS_ROOT / name] = embedded[key]
        if missing:
            raise FileNotFoundError(f"Missing top docs in defaults: {', '.join(missing)}")
        return docs
    docs: dict[Path, str] = {}
    missing: list[str] = []
    for name in TOP_DOC_FILENAMES:
        src_path = SRC_DEFAULT_TOP_DOCS_DIR / name
        if not src_path.exists():
            missing.append(name)
            continue
        docs[ATLAS_ROOT / name] = read_text(src_path)
    if missing:
        raise FileNotFoundError(f"Missing top docs in defaults: {', '.join(missing)}")
    return docs


def load_default_templates() -> dict[str, str]:
    embedded = load_embedded_defaults()
    if not SRC_DEFAULT_TEMPLATES_DIR.is_dir():
        templates: dict[str, str] = {}
        missing: list[str] = []
        for name in TEMPLATE_NAMES:
            key = f"templates/{name}"
            if key not in embedded:
                missing.append(name)
                continue
            templates[name] = embedded[key]
        if missing:
            raise FileNotFoundError(f"Missing templates in defaults: {', '.join(missing)}")
        return templates
    templates: dict[str, str] = {}
    missing: list[str] = []
    for name in TEMPLATE_NAMES:
        src_path = SRC_DEFAULT_TEMPLATES_DIR / name
        if not src_path.exists():
            missing.append(name)
            continue
        templates[name] = read_text(src_path)
    if missing:
        raise FileNotFoundError(f"Missing templates in defaults: {', '.join(missing)}")
    return templates


def load_default_prompts() -> dict[str, str]:
    embedded = load_embedded_defaults()
    if not SRC_DEFAULT_PROMPTS_DIR.is_dir():
        prompts: dict[str, str] = {}
        missing: list[str] = []
        for name in PROMPT_NAMES:
            key = f"prompts/{name}"
            if key not in embedded:
                missing.append(name)
                continue
            prompts[name] = embedded[key]
        if missing:
            raise FileNotFoundError(f"Missing prompts in defaults: {', '.join(missing)}")
        return prompts
    prompts: dict[str, str] = {}
    missing: list[str] = []
    for name in PROMPT_NAMES:
        src_path = SRC_DEFAULT_PROMPTS_DIR / name
        if not src_path.exists():
            missing.append(name)
            continue
        prompts[name] = read_text(src_path)
    if missing:
        raise FileNotFoundError(f"Missing prompts in defaults: {', '.join(missing)}")
    return prompts


def load_default_dir_readmes() -> dict[Path, str]:
    embedded = load_embedded_defaults()
    if not SRC_DEFAULT_DIR_READMES_DIR.is_dir():
        docs: dict[Path, str] = {}
        missing: list[str] = []
        for rel_path in DIR_README_PATHS:
            key = f"dir_readmes/{rel_path.as_posix()}"
            if key not in embedded:
                missing.append(str(rel_path))
                continue
            docs[ATLAS_ROOT / rel_path] = embedded[key]
        if missing:
            raise FileNotFoundError(f"Missing dir READMEs in defaults: {', '.join(missing)}")
        return docs
    docs: dict[Path, str] = {}
    missing: list[str] = []
    for rel_path in DIR_README_PATHS:
        src_path = SRC_DEFAULT_DIR_READMES_DIR / rel_path
        if not src_path.exists():
            missing.append(str(rel_path))
            continue
        docs[ATLAS_ROOT / rel_path] = read_text(src_path)
    if missing:
        raise FileNotFoundError(f"Missing dir READMEs in defaults: {', '.join(missing)}")
    return docs


def load_default_system_files() -> dict[str, str]:
    """Load VERSION and VERSIONING.md from src/.system_defaults/."""
    files: dict[str, str] = {}
    for name in ["VERSION", "VERSIONING.md", "CHANGELOG.md"]:
        src_path = SRC_DEFAULTS_ROOT / name
        if src_path.exists():
            files[name] = read_text(src_path)
        else:
            embedded = load_embedded_defaults()
            if name in embedded:
                files[name] = embedded[name]
    return files


def load_default_src_files() -> dict[str, str]:
    """Load source files - either from defaults dir or embedded in atlas.py."""
    import base64
    files: dict[str, str] = {}
    
    # Try loading from src/.system_defaults/src/ first (development mode)
    src_dir = SRC_DEFAULTS_ROOT / "src"
    if src_dir.is_dir():
        for path in src_dir.glob("*.py"):
            files[path.name] = read_text(path)
    
    # If no files found, try embedded source (distribution mode)
    if not files and EMBEDDED_SRC_B64 != "__EMBEDDED_SRC_PLACEHOLDER__":
        try:
            decoded = base64.b64decode(EMBEDDED_SRC_B64).decode("utf-8")
            files["atlas_cli.py"] = decoded
        except Exception:
            pass
    
    return files


def load_template(name: str) -> str:
    template_path = TEMPLATES_DIR / name
    if not template_path.exists():
        raise FileNotFoundError(f"Missing template: {template_path}")
    return read_text(template_path)


def iter_md_files(dirs: Iterable[Path]) -> list[Path]:
    files: list[Path] = []
    for base in dirs:
        if not base.is_dir():
            continue
        for path in base.rglob("*.md"):
            files.append(path)
    return files


def extract_meta(text: str) -> dict[str, str]:
    meta: dict[str, str] = {}
    head = "\n".join(text.splitlines()[:60])
    for line in head.splitlines():
        match = META_RE.match(line.strip())
        if match:
            meta[match.group(1).strip()] = match.group(2).strip()
    return meta


def extract_header_id(text: str) -> Optional[str]:
    match = HEADER_ID_RE.search(text)
    return match.group(1).strip() if match else None


def parse_must_read(value: str) -> list[str]:
    raw = value.strip()
    if raw.lower() == "none":
        return []
    tokens = [t.strip() for t in raw.split(",") if t.strip()]
    ids: list[str] = []
    for token in tokens:
        if token.startswith("[") and "]" in token and "(" in token:
            token = token[1 : token.index("]")].strip()
        if token:
            ids.append(token)
    return ids


def next_id(prefix: str, domain: str, dir_path: Path, pattern: re.Pattern) -> str:
    max_n = 0
    if dir_path.exists():
        for path in dir_path.glob(f"{prefix}-{domain}-*.md"):
            match = pattern.match(path.stem)
            if match:
                num = int(match.group(2))
                if num > max_n:
                    max_n = num
    return f"{prefix}-{domain}-{max_n + 1:03d}"


def next_run_step(req_id: str) -> int:
    match = REQ_ID_PATTERN.match(req_id)
    if not match:
        return 1
    domain = match.group(1)
    number = match.group(2)
    max_step = 0
    if RUN_DIR.exists():
        for path in RUN_DIR.glob(f"RUN-REQ-{domain}-{number}-step-*.md"):
            run_match = RUN_ID_PATTERN.match(path.stem)
            if run_match and run_match.group(1) == "REQ":
                step = int(run_match.group(4))
                if step > max_step:
                    max_step = step
    return max_step + 1


def update_meta_line(text: str, key: str, value: str) -> str:
    lines = text.splitlines()
    updated = False
    for i, line in enumerate(lines):
        if line.startswith("> **") and line.split("**", 2)[1].strip() == key:
            lines[i] = f"> **{key}**: {value}"
            updated = True
            break
    if not updated:
        insert_at = 1 if lines else 0
        lines.insert(insert_at, f"> **{key}**: {value}")
    return "\n".join(lines) + "\n"


def normalize_status(value: str) -> str:
    return value.strip().lower()


def parse_completed_date(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    raw = value.strip()
    if raw == "-":
        return None
    try:
        return datetime.strptime(raw, "%Y-%m-%d")
    except ValueError:
        return None


def parse_affected_artifacts(text: str) -> dict[str, list[str]]:
    artifacts = {"Create": [], "Modify": [], "Read": []}
    for line in text.splitlines():
        line = line.strip()
        for key in artifacts.keys():
            prefix = f"- {key}:"
            if line.startswith(prefix):
                remainder = line[len(prefix) :].strip()
                if remainder:
                    parts = [p.strip() for p in remainder.split(",") if p.strip()]
                    artifacts[key].extend(parts)
    return artifacts


def update_brief_status(brief_id: str, status: str) -> bool:
    if not BRIEF_ID_PATTERN.match(brief_id):
        print(f"[WARN] Invalid BRIEF ID in RUN meta: {brief_id}")
        return False
    brief_path = BRIEF_DIR / f"{brief_id}.md"
    if not brief_path.exists():
        print(f"[WARN] BRIEF not found for RUN: {brief_path}")
        return False
    brief_text = read_text(brief_path)
    brief_text = update_meta_line(brief_text, "Status", status)
    write_text(brief_path, brief_text)
    print(f"[OK] Updated {brief_path}")
    return True


def extract_ids_from_text(text: str) -> list[str]:
    return re.findall(r"(?:REQ|RULE|ADR|CQ|BRIEF|RUN)-[A-Z]+-\d{3}(?:-step-\d{2})?", text)


def derive_title(text: str, fallback: str = "User Request") -> str:
    title_src = " ".join(text.strip().splitlines()).strip()
    if not title_src:
        return fallback
    return title_src[:60] + ("..." if len(title_src) > 60 else "")


def is_relative_to(path: Path, base: Path) -> bool:
    try:
        path.relative_to(base)
        return True
    except ValueError:
        return False


def req_id_from_run_id(run_id: str) -> Optional[str]:
    match = RUN_ID_PATTERN.match(run_id)
    if not match:
        return None
    kind, domain, number, _step = match.groups()
    if kind != "REQ":
        return None
    return f"REQ-{domain}-{number}"


def detect_git_hash() -> Optional[str]:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
    except Exception:
        return None
    value = result.stdout.strip()
    return value if value else None


def write_last_run(state: dict) -> None:
    ensure_dir(STATE_DIR)
    write_text(LAST_RUN_PATH, json.dumps(state, indent=2) + "\n")


# =============================================================================
# Sync utilities
# =============================================================================

def parse_checkboxes(text: str) -> list[tuple[int, bool, str]]:
    """Parse checkboxes from text. Returns list of (line_num, is_checked, content)."""
    results = []
    for i, line in enumerate(text.splitlines()):
        if CHECKBOX_CHECKED.match(line):
            match = CHECKBOX_CHECKED.match(line)
            results.append((i, True, match.group(2).strip()))
        elif CHECKBOX_UNCHECKED.match(line):
            match = CHECKBOX_UNCHECKED.match(line)
            results.append((i, False, match.group(2).strip()))
    return results


def parse_traceability(text: str) -> dict[str, tuple[str, str]]:
    """Parse traceability links. Returns {link_type: (id, path)}."""
    results = {}
    for match in TRACEABILITY_LINK_RE.finditer(text):
        link_id = match.group(1).strip()
        link_path = match.group(2).strip()
        # Determine link type from context
        full_match = match.group(0)
        if "Implements" in full_match:
            results["Implements"] = (link_id, link_path)
        elif "Answers" in full_match:
            results["Answers"] = (link_id, link_path)
        elif "Solved by" in full_match:
            results["Solved by"] = (link_id, link_path)
        elif "Implemented by" in full_match:
            results["Implemented by"] = (link_id, link_path)
    return results


def resolve_linked_docs(run_path: Path) -> dict[str, Path]:
    """Resolve RUN -> BRIEF -> REQ chain. Returns {doc_type: path}."""
    docs = {}
    text = read_text(run_path)
    meta = extract_meta(text)

    # RUN -> REQ (direct)
    req_id = meta.get("REQ") or req_id_from_run_id(run_path.stem)
    if req_id and REQ_ID_PATTERN.match(req_id):
        req_path = REQ_DIR / f"{req_id}.md"
        if req_path.exists():
            docs["REQ"] = req_path
    
    # RUN -> BRIEF
    brief_id = meta.get("Brief")
    if brief_id and BRIEF_ID_PATTERN.match(brief_id):
        brief_path = BRIEF_DIR / f"{brief_id}.md"
        if brief_path.exists():
            docs["BRIEF"] = brief_path
            
            # BRIEF -> REQ (via Implements link)
            brief_text = read_text(brief_path)
            trace = parse_traceability(brief_text)
            if "Implements" in trace:
                req_id, req_rel_path = trace["Implements"]
                req_path = (brief_path.parent / req_rel_path).resolve()
                if req_path.exists():
                    docs["REQ"] = req_path
    
    return docs


def compute_status_from_checkboxes(text: str) -> Optional[str]:
    """Compute status based on checkbox completion in Steps/Verification sections."""
    checkboxes = parse_checkboxes(text)
    if not checkboxes:
        return None
    
    total = len(checkboxes)
    checked = sum(1 for _, is_checked, _ in checkboxes if is_checked)
    
    if checked == 0:
        return "Planned"
    elif checked == total:
        return "Completed"
    else:
        return "InProgress"


def generate_sync_diff(run_path: Path) -> dict:
    """Generate diff for sync operation. Returns changes to apply."""
    diff = {
        "run": {"path": run_path, "changes": []},
        "brief": None,
        "req": None,
    }
    
    run_text = read_text(run_path)
    run_meta = extract_meta(run_text)
    run_checkboxes = parse_checkboxes(run_text)
    
    # Compute RUN status from checkboxes
    computed_status = compute_status_from_checkboxes(run_text)
    current_status = run_meta.get("Status", "")
    
    if computed_status and normalize_status(computed_status) != normalize_status(current_status):
        diff["run"]["changes"].append({
            "type": "status",
            "from": current_status,
            "to": computed_status,
        })
    
    # Resolve linked documents
    linked = resolve_linked_docs(run_path)
    
    # BRIEF sync
    if "BRIEF" in linked:
        brief_path = linked["BRIEF"]
        brief_text = read_text(brief_path)
        brief_meta = extract_meta(brief_text)
        brief_status = brief_meta.get("Status", "")
        
        diff["brief"] = {
            "path": brief_path,
            "changes": [],
        }
        
        # Sync status
        if computed_status and normalize_status(brief_status) != normalize_status(computed_status):
            diff["brief"]["changes"].append({
                "type": "status",
                "from": brief_status,
                "to": computed_status,
            })
    
    # REQ patch (don't auto-modify, generate patch)
    if "REQ" in linked:
        req_path = linked["REQ"]
        req_text = read_text(req_path)
        req_meta = extract_meta(req_text)
        req_checkboxes = parse_checkboxes(req_text)
        
        diff["req"] = {
            "path": req_path,
            "changes": [],
            "checkboxes": req_checkboxes,
        }
        
        # Check if REQ acceptance criteria should be updated based on RUN completion
        if computed_status == "Completed" and req_checkboxes:
            # Suggest marking related checkboxes
            diff["req"]["changes"].append({
                "type": "checkbox_suggestion",
                "message": f"RUN completed. Consider updating acceptance criteria in {req_path.name}",
            })
    
    return diff


def print_sync_diff(diff: dict) -> None:
    """Print sync diff in human-readable format."""
    run_info = diff["run"]
    print(f"\n[SYNC] {run_info['path'].stem}")
    
    if run_info["changes"]:
        for change in run_info["changes"]:
            if change["type"] == "status":
                print(f"  → RUN: Status {change['from']} → {change['to']}")
    else:
        print("  → RUN: (no changes)")
    
    if diff["brief"]:
        brief_info = diff["brief"]
        if brief_info["changes"]:
            for change in brief_info["changes"]:
                if change["type"] == "status":
                    print(f"  → BRIEF ({brief_info['path'].stem}): Status {change['from']} → {change['to']}")
        else:
            print(f"  → BRIEF ({brief_info['path'].stem}): (no changes)")
    
    if diff["req"]:
        req_info = diff["req"]
        if req_info["changes"]:
            for change in req_info["changes"]:
                if change["type"] == "checkbox_suggestion":
                    print(f"  → REQ ({req_info['path'].stem}): [Patch required] {change['message']}")
        else:
            print(f"  → REQ ({req_info['path'].stem}): (no changes)")


def apply_brief_changes(diff: dict) -> bool:
    """Apply changes to BRIEF document."""
    if not diff["brief"] or not diff["brief"]["changes"]:
        return False
    
    brief_path = diff["brief"]["path"]
    brief_text = read_text(brief_path)
    
    for change in diff["brief"]["changes"]:
        if change["type"] == "status":
            brief_text = update_meta_line(brief_text, "Status", change["to"])
    
    write_text(brief_path, brief_text)
    print(f"[OK] Updated {brief_path}")
    return True


def write_req_patch(diff: dict) -> Optional[Path]:
    """Write REQ patch file."""
    if not diff["req"] or not diff["req"]["changes"]:
        return None
    
    ensure_dir(PATCH_DIR)
    req_path = diff["req"]["path"]
    patch_path = PATCH_DIR / f"{req_path.stem}.patch.md"
    
    content = f"""# Patch for {req_path.stem}

> **Generated**: {now_date()}
> **Source RUN**: {diff['run']['path'].stem}

## Suggested Changes

"""
    for change in diff["req"]["changes"]:
        if change["type"] == "checkbox_suggestion":
            content += f"- {change['message']}\n"
    
    content += f"""
## How to Apply

```bash
atlas sync {diff['run']['path'].stem} --apply-req
```

Or manually edit: {req_path}
"""
    
    write_text(patch_path, content)
    print(f"[OK] Created patch: {patch_path}")
    return patch_path


def apply_req_changes(diff: dict) -> bool:
    """Apply changes to REQ document (with warning)."""
    if not diff["req"] or not diff["req"]["changes"]:
        return False
    
    print("[WARN] Modifying REQ document (authority document)")
    req_path = diff["req"]["path"]
    req_text = read_text(req_path)
    
    # For now, just update status if RUN is completed
    run_changes = diff["run"]["changes"]
    for change in run_changes:
        if change["type"] == "status" and change["to"] == "Completed":
            req_text = update_meta_line(req_text, "Status", "Implemented")
    
    write_text(req_path, req_text)
    print(f"[OK] Updated {req_path}")
    return True


def init_command(_args: argparse.Namespace) -> int:
    overwrite = getattr(_args, "overwrite", False)
    ensure_dir(ATLAS_ROOT)
    for d in [
        REQ_DIR,
        RULE_DIR,
        ADR_DIR,
        CQ_DIR,
        VIEWS_DIR,
        INBOX_DIR,
        DRAFTS_DIR,
        BRIEF_DIR,
        RUN_DIR,
        ARCHIVE_DIR,
        TEMPLATES_DIR,
        STATE_DIR,
        SYSTEM_ROOT / "prompts",
        SYSTEM_ROOT / "src",
    ]:
        ensure_dir(d)

    # README files in directories - system files, no backup needed
    for readme_path, content in load_default_dir_readmes().items():
        if overwrite or not readme_path.exists():
            write_text(readme_path, content)
            if overwrite:
                print(f"[OK] Updated {readme_path}")
            else:
                print(f"[OK] Created {readme_path}")

    # Top docs - USER-EDITABLE, backup before overwrite
    for path, content in load_default_top_docs().items():
        if overwrite or not path.exists():
            if overwrite and path.exists():
                backup = backup_file(path)
                if backup:
                    print(f"[INFO] Backed up {path.name} to archive/")
            
            write_text(path, content)
            print(f"[OK] {'Updated' if overwrite else 'Created'} {path}")

    # Templates - system files, no backup needed
    for name, content in load_default_templates().items():
        template_path = TEMPLATES_DIR / name
        if overwrite or not template_path.exists():
            write_text(template_path, content)

    # Prompts - system files, no backup needed
    prompts_dir = SYSTEM_ROOT / "prompts"
    for name, content in load_default_prompts().items():
        prompt_path = prompts_dir / name
        if overwrite or not prompt_path.exists():
            write_text(prompt_path, content)
            print(f"[OK] {'Updated' if overwrite else 'Created'} {prompt_path}")

    for name, content in load_default_system_files().items():
        system_path = SYSTEM_ROOT / name
        if overwrite or not system_path.exists():
            write_text(system_path, content)
            print(f"[OK] Created {system_path}")

    src_dir = SYSTEM_ROOT / "src"
    for name, content in load_default_src_files().items():
        src_path = src_dir / name
        if overwrite or not src_path.exists():
            write_text(src_path, content)
            print(f"[OK] Created {src_path}")

    if not LAST_RUN_PATH.exists():
        write_last_run({"stage": "idle", "updated_at": now_iso()})

    print("[OK] Atlas structure initialized.")
    print("[INFO] Run the prompt in .atlas/.system/prompts/onboarding.md to complete setup.")
    return 0


def create_brief_doc(text: str, domain: str) -> Path:
    brief_id = next_id("BRIEF", domain, BRIEF_DIR, BRIEF_ID_PATTERN)
    title = derive_title(text)
    content = f"""# [{brief_id}] {title}

> **ID**: {brief_id}
> **Domain**: {domain}
> **Status**: Active
> **Date**: {now_date()}

## 1. User Request
{text.strip()}

## 2. Intent Summary
- Goal: 
- Problem: 

## 3. Affected Artifacts
- Create: 
- Modify: 
- Read: 

## 4. Proposed Changes
1. 
2. 

## 5. Verification Criteria
- [ ] 
"""
    path = BRIEF_DIR / f"{brief_id}.md"
    ensure_dir(BRIEF_DIR)
    write_text(path, content)
    return path


def capture_command(args: argparse.Namespace) -> int:
    domain = args.domain.upper()
    text = args.text.strip()
    if not text:
        print("[ERR] Empty input.")
        return 1

    title = derive_title(text)
    req_ids = [rid for rid in extract_ids_from_text(text) if rid.startswith("REQ-")]
    if not req_ids:
        req_ids = [next_id("REQ", domain, REQ_DIR, REQ_ID_PATTERN)]

    created = []
    for req_id in req_ids:
        if not REQ_ID_PATTERN.match(req_id):
            print(f"[WARN] Skipping invalid REQ ID: {req_id}")
            continue
        create_req_stub(req_id, title=title)
        req_path = REQ_DIR / f"{req_id}.md"
        if req_path.exists():
            append_capture_note(req_path, text)
        view_path = ensure_view_doc(req_id, title)
        created.append((req_path, view_path))

    if getattr(args, "to", None) == "brief":
        brief_path = create_brief_doc(text, domain)
        print(f"[OK] Created {brief_path}")

    for req_path, view_path in created:
        print(f"[OK] Updated {req_path}")
        print(f"[OK] Updated {view_path}")
    return 0


def create_req_stub(req_id: str, title: Optional[str] = None) -> None:
    path = REQ_DIR / f"{req_id}.md"
    if path.exists():
        return
    match = REQ_ID_PATTERN.match(req_id)
    if not match:
        return
    domain = match.group(1)
    template = load_template("REQ.md")
    title = title or "Title"
    content = template.replace("REQ-XXX-001", req_id)
    content = content.replace("# [REQ-XXX-001] Title", f"# [{req_id}] {title}")
    content = content.replace("Domain**: XXX", f"Domain**: {domain}")
    content = content.replace("Last Updated**: YYYY-MM-DD", f"Last Updated**: {now_date()}")
    write_text(path, content)


def append_capture_note(path: Path, text: str) -> None:
    note = text.strip()
    if not note:
        return
    content = read_text(path)
    stamp = now_date()
    block = f"\n## Capture ({stamp})\n{note}\n"
    if f"## Capture ({stamp})" in content:
        return
    write_text(path, content.rstrip() + block)


def ensure_view_doc(req_id: str, title: str) -> Path:
    path = VIEWS_DIR / f"{req_id}.md"
    if not path.exists():
        template = load_template("VIEW.md")
        content = template.replace("REQ-XXX-001", req_id)
        content = content.replace("# [VIEW-REQ-XXX-001] Title", f"# [VIEW-{req_id}] {title}")
        content = content.replace("Last Updated**: YYYY-MM-DD", f"Last Updated**: {now_date()}")
        write_text(path, content)
        return path

    content = read_text(path)
    if req_id not in content:
        if "## References (SSOT index)" not in content:
            content = content.rstrip() + "\n\n## References (SSOT index)\n"
        content = content.rstrip() + f"\n- {req_id}\n"
        write_text(path, content)
    return path


def extract_section_lines(text: str, heading: str) -> list[str]:
    lines = text.splitlines()
    out: list[str] = []
    in_section = False
    target = f"## {heading}".strip().lower()
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## "):
            if in_section:
                break
            in_section = stripped.lower() == target
            continue
        if in_section:
            out.append(line)
    return out


def extract_view_references(text: str) -> set[str]:
    refs: set[str] = set()
    for line in extract_section_lines(text, "References (SSOT index)"):
        for ref_id in SSOT_ID_RE.findall(line):
            refs.add(ref_id)
    return refs


def extract_view_summary_refs(text: str) -> set[str]:
    refs: set[str] = set()
    for line in extract_section_lines(text, "Summary"):
        if "<!--" in line:
            continue
        for match in REF_TOKEN_RE.finditer(line):
            refs.add(match.group("id"))
    return refs


def extract_view_ssot_refs(text: str) -> set[str]:
    meta = extract_meta(text)
    value = meta.get("Refs", "") or meta.get("SSOT", "")
    return set(SSOT_ID_RE.findall(value))


def ssot_path_for_id(ref_id: str) -> Optional[Path]:
    prefix = ref_id.split("-", 1)[0]
    if prefix == "REQ":
        return REQ_DIR / f"{ref_id}.md"
    if prefix == "RULE":
        return RULE_DIR / f"{ref_id}.md"
    if prefix == "ADR":
        return ADR_DIR / f"{ref_id}.md"
    return None


def run_command(args: argparse.Namespace) -> int:
    req_id = args.req_id
    if req_id.endswith(".md"):
        req_id = Path(req_id).stem

    match = REQ_ID_PATTERN.match(req_id)
    if not match:
        print(f"[ERR] Invalid REQ ID: {req_id}")
        return 1

    req_path = REQ_DIR / f"{req_id}.md"
    if not req_path.exists():
        print(f"[ERR] REQ not found: {req_path}")
        return 1

    domain = match.group(1)
    number = match.group(2)
    step = getattr(args, "step", None) or next_run_step(req_id)
    run_id = f"RUN-REQ-{domain}-{number}-step-{int(step):02d}"
    run_path = RUN_DIR / f"{run_id}.md"
    if run_path.exists():
        print(f"[ERR] RUN already exists: {run_path}")
        return 1

    content = f"""# [{run_id}] Plan

> **ID**: {run_id}
> **REQ**: {req_id}
> **Status**: Planned
> **Started**: {now_date()}
> **Git**: -
> **Completed**: -

## Target REQ
- {req_id}

## Plan
- [ ] 

## Verification
- [ ] Test
- [ ] Spec
- [ ] Boundary

## Output
- (files created/modified)
"""
    write_text(run_path, content)

    write_last_run(
        {
            "run_id": run_id,
            "req_id": req_id,
            "stage": "executing",
            "updated_at": now_iso(),
        }
    )

    print(f"[OK] Created {run_path}")
    return 0


def plan_command(args: argparse.Namespace) -> int:
    print("[WARN] 'plan' is deprecated. Use 'run' instead.")
    args.req_id = args.brief_id
    return run_command(args)


def finish_command(args: argparse.Namespace) -> int:
    run_id = args.run_id
    if run_id.endswith(".md"):
        run_id = Path(run_id).stem

    if not RUN_ID_PATTERN.match(run_id):
        print(f"[ERR] Invalid RUN ID: {run_id}")
        return 1

    run_path = RUN_DIR / f"{run_id}.md"
    if not run_path.exists():
        print(f"[ERR] RUN not found: {run_path}")
        return 1

    git_hash = args.git
    if not git_hash:
        git_hash = detect_git_hash()
    if not git_hash:
        print("[ERR] Missing git hash. Provide --git or ensure git is available.")
        return 1

    text = read_text(run_path)
    meta = extract_meta(text)
    brief_id = meta.get("Brief")
    req_id = meta.get("REQ") or req_id_from_run_id(run_id)
    status = "Completed" if args.success else "Failed"
    text = update_meta_line(text, "Status", status)
    text = update_meta_line(text, "Git", git_hash)
    text = update_meta_line(text, "Completed", now_date())
    write_text(run_path, text)

    if brief_id:
        update_brief_status(brief_id, status)

    if req_id:
        req_path = REQ_DIR / f"{req_id}.md"
        if req_path.exists():
            req_text = read_text(req_path)
            req_text = update_meta_line(req_text, "Implemented-Git", git_hash)
            req_text = update_meta_line(req_text, "Linked-RUN", run_id)
            req_text = update_meta_line(req_text, "Last Updated", now_date())
            write_text(req_path, req_text)
            print(f"[OK] Updated {req_path}")

    last_run_state = {
        "run_id": run_id,
        "stage": "finished",
        "git_hash": git_hash,
        "completed_at": now_iso(),
    }
    if brief_id:
        last_run_state["brief_id"] = brief_id
    if req_id:
        last_run_state["req_id"] = req_id
    write_last_run(last_run_state)

    print(f"[OK] Updated {run_path}")
    return 0


def sync_command(args: argparse.Namespace) -> int:
    """Sync RUN status to BRIEF/REQ documents."""
    run_id = args.run_id
    if run_id.endswith(".md"):
        run_id = Path(run_id).stem

    if not RUN_ID_PATTERN.match(run_id):
        print(f"[ERR] Invalid RUN ID: {run_id}")
        return 1

    run_path = RUN_DIR / f"{run_id}.md"
    if not run_path.exists():
        print(f"[ERR] RUN not found: {run_path}")
        return 1

    # Generate diff
    diff = generate_sync_diff(run_path)
    
    # Always print diff (dry-run info)
    print_sync_diff(diff)
    
    # Check if any apply flags are set
    apply_brief = getattr(args, "apply_brief", False)
    apply_req = getattr(args, "apply_req", False)
    write_patch = getattr(args, "write_req_patch", False)
    
    if not (apply_brief or apply_req or write_patch):
        print("\n[INFO] Dry-run mode. Use --apply-brief, --write-req-patch, or --apply-req to make changes.")
        return 0
    
    # Apply RUN changes (always when any apply flag is set)
    if diff["run"]["changes"]:
        run_text = read_text(run_path)
        for change in diff["run"]["changes"]:
            if change["type"] == "status":
                run_text = update_meta_line(run_text, "Status", change["to"])
        write_text(run_path, run_text)
        print(f"[OK] Updated {run_path}")
    
    # Apply BRIEF changes
    if apply_brief:
        apply_brief_changes(diff)
    
    # Write REQ patch
    if write_patch:
        write_req_patch(diff)
    
    # Apply REQ changes (with warning)
    if apply_req:
        apply_req_changes(diff)
    
    return 0


def iter_links(text: str) -> list[str]:
    links = []
    in_code = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        for match in LINK_RE.finditer(line):
            links.append(match.group(1).strip())
    return links


def doctor_command(args: argparse.Namespace) -> int:
    issues = 0
    brief_statuses: dict[str, str] = {}
    run_brief_statuses: list[tuple[str, str, str, Optional[datetime]]] = []

    required_dirs = [
        REQ_DIR,
        RULE_DIR,
        ADR_DIR,
        CQ_DIR,
        VIEWS_DIR,
        INBOX_DIR,
        DRAFTS_DIR,
        BRIEF_DIR,
        RUN_DIR,
        ARCHIVE_DIR,
        SYSTEM_ROOT,
        TEMPLATES_DIR,
        STATE_DIR,
    ]
    for path in required_dirs:
        if not path.exists():
            print(f"[ERR] Missing directory: {path}")
            issues += 1

    for path in REQUIRED_TOP_DOCS:
        if not path.exists():
            print(f"[ERR] Missing top doc: {path}")
            issues += 1

    for path in OPTIONAL_TOP_DOCS:
        if not path.exists():
            print(f"[WARN] Missing optional doc: {path}")

    scan_dirs = [REQ_DIR, RULE_DIR, ADR_DIR, CQ_DIR, BRIEF_DIR, RUN_DIR]
    all_docs = iter_md_files(scan_dirs)
    all_ids: set[str] = set()

    for path in all_docs:
        text = read_text(path)
        meta = extract_meta(text)
        meta_id = meta.get("ID")
        header_id = extract_header_id(text)
        file_id = path.stem
        for candidate in [meta_id, header_id, file_id]:
            if candidate:
                all_ids.add(candidate)

    for path in all_docs:
        text = read_text(path)
        meta = extract_meta(text)
        meta_id = meta.get("ID")
        header_id = extract_header_id(text)
        file_id = path.stem

        folder = path.parent.name
        expected_prefix = {
            "req": "REQ",
            "rule": "RULE",
            "adr": "ADR",
            "cq": "CQ",
            "brief": "BRIEF",
            "runs": "RUN",
        }.get(folder)

        if expected_prefix is None:
            continue

        if expected_prefix == "BRIEF":
            status = meta.get("Status")
            if not status:
                print(f"[ERR] Missing Status: {path}")
                issues += 1
            else:
                brief_statuses[file_id] = status

        if expected_prefix == "RUN":
            brief_id = meta.get("Brief")
            run_status = meta.get("Status")
            completed = meta.get("Completed")
            if brief_id and run_status:
                run_brief_statuses.append(
                    (file_id, brief_id, run_status, parse_completed_date(completed))
                )
            if file_id.startswith("RUN-BRIEF-") and not brief_id:
                print(f"[WARN] Missing Brief reference: {path}")
                issues += 1

        if not meta_id:
            print(f"[ERR] Missing meta ID: {path}")
            issues += 1
        if not header_id:
            print(f"[ERR] Missing header ID: {path}")
            issues += 1

        pattern = {
            "REQ": REQ_ID_PATTERN,
            "RULE": RULE_ID_PATTERN,
            "ADR": ADR_ID_PATTERN,
            "CQ": CQ_ID_PATTERN,
            "BRIEF": BRIEF_ID_PATTERN,
            "RUN": RUN_ID_PATTERN,
        }[expected_prefix]

        if not pattern.match(file_id):
            print(f"[ERR] Invalid filename for {expected_prefix}: {path}")
            issues += 1

        if meta_id and meta_id != file_id:
            print(f"[ERR] Meta ID mismatch: {path}")
            issues += 1
        if header_id and header_id != file_id:
            print(f"[ERR] Header ID mismatch: {path}")
            issues += 1

        if expected_prefix in {"REQ", "RULE"}:
            must_read = meta.get("Must-Read")
            if must_read is None:
                print(f"[ERR] Missing Must-Read: {path}")
                issues += 1
            else:
                ids = parse_must_read(must_read)
                if not ids and must_read.strip().lower() != "none":
                    print(f"[ERR] Empty Must-Read: {path}")
                    issues += 1
                for ref_id in ids:
                    prefix = ref_id.split("-", 1)[0]
                    if prefix not in ALLOWED_MUST_READ_PREFIXES:
                        print(f"[ERR] Must-Read disallowed ID: {path} -> {ref_id}")
                        issues += 1
                    if ref_id not in all_ids:
                        print(f"[ERR] Must-Read missing target: {path} -> {ref_id}")
                        issues += 1

        if expected_prefix == "REQ":
            status = meta.get("Status", "")
            implemented_git = meta.get("Implemented-Git", "").strip()
            if normalize_status(status) == "implemented" and (not implemented_git or implemented_git == "-"):
                print(f"[WARN] Implemented REQ missing git hash: {path}")
                issues += 1

        if args.links:
            for target in iter_links(text):
                if not target or target.startswith("#"):
                    continue
                if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                    continue
                resolved = (path.parent / target).resolve()
                if not resolved.exists():
                    print(f"[ERR] Broken link: {path} -> {target}")
                    issues += 1

    # View -> REQ link validation
    view_refs: set[str] = set()
    for path in iter_md_files([VIEWS_DIR]):
        text = read_text(path)
        index_refs = extract_view_references(text)
        summary_refs = extract_view_summary_refs(text)
        ssot_refs = extract_view_ssot_refs(text)
        summary_lines = extract_section_lines(text, "Summary")

        if not index_refs:
            print(f"[WARN] View missing References (SSOT index): {path}")
            issues += 1

        if not ssot_refs:
            print(f"[WARN] View missing Refs meta: {path}")
            issues += 1

        for ref_id in ssot_refs:
            if ref_id not in index_refs:
                print(f"[WARN] Refs not in SSOT index: {path} -> {ref_id}")
                issues += 1
            ref_path = ssot_path_for_id(ref_id)
            if not ref_path or not ref_path.exists():
                print(f"[WARN] Refs missing SSOT: {path} -> {ref_id}")
                issues += 1

        for ref_id in index_refs:
            ref_path = ssot_path_for_id(ref_id)
            if not ref_path or not ref_path.exists():
                print(f"[WARN] View refs missing SSOT: {path} -> {ref_id}")
                issues += 1

        for ref_id in summary_refs:
            if ref_id not in index_refs:
                print(f"[WARN] Summary ref not in SSOT index: {path} -> {ref_id}")
                issues += 1
            ref_path = ssot_path_for_id(ref_id)
            if not ref_path or not ref_path.exists():
                print(f"[WARN] Summary ref missing SSOT: {path} -> {ref_id}")
                issues += 1

        for line in summary_lines:
            if "<!--" in line:
                continue
            if "ATLAS:OK" in line and not REF_TOKEN_RE.search(line):
                print(f"[WARN] Summary line marked ATLAS:OK missing ref: {path}")
                issues += 1
            if any(keyword in line for keyword in NORMATIVE_KEYWORDS) and not REF_TOKEN_RE.search(line):
                print(f"[WARN] Summary line has normative keyword without ref: {path}")
                issues += 1

        view_refs.update(index_refs | summary_refs | ssot_refs)

        for target in iter_links(text):
            if not target or target.startswith("#"):
                continue
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                continue
            resolved = (path.parent / target).resolve()
            if (
                (is_relative_to(resolved, REQ_DIR) or is_relative_to(resolved, RULE_DIR) or is_relative_to(resolved, ADR_DIR))
                and not resolved.exists()
            ):
                print(f"[WARN] Broken SSOT link in view: {path} -> {target}")
                issues += 1

    # REQ without any view reference
    req_ids = [path.stem for path in all_docs if path.parent.name == "req"]
    for req_id in req_ids:
        if req_id not in view_refs:
            print(f"[WARN] Missing view reference for REQ: {req_id}")
            issues += 1

    latest_run_by_brief: dict[str, tuple[str, str, Optional[datetime]]] = {}
    for run_id, brief_id, run_status, completed_at in run_brief_statuses:
        normalized = normalize_status(run_status)
        if normalized not in {"completed", "failed"}:
            continue
        existing = latest_run_by_brief.get(brief_id)
        if existing is None:
            latest_run_by_brief[brief_id] = (run_id, run_status, completed_at)
            continue
        existing_run_id, _, existing_completed = existing
        if completed_at and (existing_completed is None or completed_at > existing_completed):
            latest_run_by_brief[brief_id] = (run_id, run_status, completed_at)
        elif completed_at is None and existing_completed is None and run_id > existing_run_id:
            latest_run_by_brief[brief_id] = (run_id, run_status, completed_at)

    for brief_id, (run_id, run_status, _) in latest_run_by_brief.items():
        brief_status = brief_statuses.get(brief_id)
        if not brief_status:
            print(f"[WARN] BRIEF missing for RUN: {run_id} -> {brief_id}")
            issues += 1
            continue
        if normalize_status(brief_status) != normalize_status(run_status):
            print(
                f"[WARN] BRIEF status mismatch: {brief_id} is {brief_status}, latest RUN {run_id} is {run_status}"
            )
            issues += 1

    if LAST_RUN_PATH.exists():
        try:
            state = json.loads(read_text(LAST_RUN_PATH))
        except json.JSONDecodeError:
            state = {}
            print(f"[ERR] Invalid JSON: {LAST_RUN_PATH}")
            issues += 1
        stage = state.get("stage")
        updated_at = state.get("updated_at") or state.get("completed_at")
        if stage == "executing" and updated_at:
            try:
                ts = datetime.fromisoformat(updated_at)
                if datetime.now() - ts > timedelta(hours=args.max_age_hours):
                    print(
                        f"[WARN] RUN may be unfinished (>{args.max_age_hours}h): {state.get('run_id')}"
                    )
                    issues += 1
            except ValueError:
                print("[ERR] Invalid timestamp in last_run.json")
                issues += 1

    print(f"[DONE] Doctor completed with {issues} issue(s).")
    return 0 if issues == 0 else 1


    print(f"[DONE] Doctor completed with {issues} issue(s).")
    return 0 if issues == 0 else 1


def parse_version(v: str) -> tuple[int, ...]:
    try:
        return tuple(map(int, v.strip().split(".")))
    except ValueError:
        return (0, 0, 0)


def check_version_update() -> None:
    """Check if Atlas has been updated and print changelog."""
    if not VERSION_PATH.exists():
        return

    installed_ver_str = VERSION_PATH.read_text(encoding="utf-8").strip()
    if not installed_ver_str:
        return

    installed_ver = parse_version(installed_ver_str)
    current_ver = parse_version(ATLAS_VERSION)

    if current_ver > installed_ver:
        print(f"\n[INFO] Upgrading Atlas: {installed_ver_str} -> {ATLAS_VERSION}")
        print("=" * 60)
        
        # Collect versions to print
        versions_to_print = []
        for ver_str in CHANGELOG:
            ver = parse_version(ver_str)
            if ver > installed_ver and ver <= current_ver:
                versions_to_print.append((ver, ver_str))
        
        # Sort by version descending
        versions_to_print.sort(key=lambda x: x[0], reverse=True)
        
        for _, ver_str in versions_to_print:
            print(f"[{ver_str}]")
            for change in CHANGELOG[ver_str]:
                print(f"- {change}")
            print()
            
        print("=" * 60)
        
        # Update VERSION file
        if VERSION_PATH.exists():
            write_text(VERSION_PATH, ATLAS_VERSION)
            print(f"[OK] Updated VERSION file to {ATLAS_VERSION}\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="atlas")
    parser.add_argument(
        "--version", "-v",
        action="version",
        version=f"Atlas {get_version()}"
    )
    sub = parser.add_subparsers(dest="command", required=False)

    init = sub.add_parser("init")
    init.add_argument("--overwrite", action="store_true")

    capture = sub.add_parser("capture")
    capture.add_argument("text")
    capture.add_argument("--domain", default="GEN")
    capture.add_argument("--to", choices=["brief"])

    intake = sub.add_parser("intake")
    intake.add_argument("text")
    intake.add_argument("--domain", default="GEN")
    intake.add_argument("--to", choices=["brief"])

    run = sub.add_parser("run")
    run.add_argument("req_id")
    run.add_argument("--step", type=int)

    plan = sub.add_parser("plan")
    plan.add_argument("brief_id")
    plan.add_argument("--step", type=int)

    finish = sub.add_parser("finish")
    finish.add_argument("run_id")
    finish.add_argument("--git")
    finish.add_argument("--success", type=lambda v: v.lower() == "true", required=True)

    doctor = sub.add_parser("doctor")
    doctor.add_argument("--links", action="store_true")
    doctor.add_argument("--max-age-hours", type=int, default=24)

    sync = sub.add_parser("sync", help="Sync RUN status to BRIEF/REQ documents")
    sync.add_argument("run_id", help="RUN document ID")
    sync.add_argument("--apply-brief", action="store_true", help="Apply changes to BRIEF document")
    sync.add_argument("--write-req-patch", action="store_true", help="Write REQ patch file")
    sync.add_argument("--apply-req", action="store_true", help="Apply changes to REQ document (caution)")

    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 0

    if args.command != "init" and not ATLAS_ROOT.exists():
        print("[INFO] .atlas not found. Initializing...")
        init_command(args)

    if args.command != "init":
        check_version_update()

    if args.command == "init":
        return init_command(args)
    if args.command == "capture":
        return capture_command(args)
    if args.command == "intake":
        print("[WARN] 'intake' is deprecated. Use 'capture' instead.")
        return capture_command(args)
    if args.command == "run":
        return run_command(args)
    if args.command == "plan":
        return plan_command(args)
    if args.command == "finish":
        return finish_command(args)
    if args.command == "doctor":
        return doctor_command(args)
    if args.command == "sync":
        return sync_command(args)

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
