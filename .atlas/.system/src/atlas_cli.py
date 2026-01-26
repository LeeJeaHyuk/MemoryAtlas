#!/usr/bin/env python3
"""Atlas vNext CLI."""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterable, Optional

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

REQ_DIR = ATLAS_ROOT / "req"
RULE_DIR = ATLAS_ROOT / "rule"
CQ_DIR = ATLAS_ROOT / "cq"
BRIEF_DIR = ATLAS_ROOT / "brief"
RUN_DIR = ATLAS_ROOT / "runs"
IDEA_DIR = ATLAS_ROOT / "idea"  # Unstructured notes, excluded from doctor

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
CQ_ID_PATTERN = re.compile(r"^CQ-([A-Z]+)-(\d{3})$")
BRIEF_ID_PATTERN = re.compile(r"^BRIEF-([A-Z]+)-(\d{3})$")
RUN_ID_PATTERN = re.compile(r"^RUN-(BRIEF|REQ)-([A-Z]+)-(\d{3})-step-(\d{2})$")

META_RE = re.compile(r"^>\s*\*\*([^*]+)\*\*:\s*(.+)$")
HEADER_ID_RE = re.compile(r"^#\s+\[([^\]]+)\]", re.M)
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")

ALLOWED_MUST_READ_PREFIXES = {"RULE"}

PATCH_DIR = ATLAS_ROOT / "patch"

# Checkbox patterns
CHECKBOX_UNCHECKED = re.compile(r"^(\s*)-\s*\[\s*\](.*)$")
CHECKBOX_CHECKED = re.compile(r"^(\s*)-\s*\[x\](.*)$", re.IGNORECASE)
TRACEABILITY_LINK_RE = re.compile(r"\*\*(?:Implements|Answers|Solved by|Implemented by)\*\*:\s*\[([^\]]+)\]\(([^)]+)\)")

DEFAULT_TOP_DOCS = {
    ATLAS_ROOT / "FRONT.md": """# Atlas\n\nThis repo uses Atlas vNext.\nUse: `python atlas.py init`\n\nQuick flow:\n1) `python atlas.py intake \"...\" --domain GEN`\n2) `python atlas.py plan BRIEF-GEN-001`\n3) `python atlas.py finish RUN-BRIEF-GEN-001-step-01 --git <hash|no-commit> --success true`\n\nLinks: BOARD.md, CONVENTIONS.md, GOALS.md\n""",
    ATLAS_ROOT / "BOARD.md": """# BOARD\n\n> 이 문서는 프로젝트의 **현재 작업 상태 스냅샷**을 나타냅니다.\n> 비어 있는 경우, 해당 상태에 해당하는 작업이 없음을 의미합니다.\n\n## Queue\n- (empty)\n\n## Active\n- (empty)\n\n## Done\n- (empty)\n\n> Last Reviewed: YYYY-MM-DD\n""",
    ATLAS_ROOT / "CONVENTIONS.md": """# CONVENTIONS\n\n## Boundaries\n\n### Always\n- Keep REQ/RULE/CQ as authority; do not auto-edit without intent.\n- Record verification steps in RUN.\n\n### Ask First\n- Add or remove dependencies.\n- Change storage layout under `.atlas/`.\n\n### Never\n- Hardcode secrets.\n- Modify existing REQ/RULE/CQ silently.\n\n## Roles (one-line)\n- REQ: what the system must do.\n- RULE: constraints that must always hold.\n- CQ: questions the system must answer.\n- BRIEF: intake summary.\n- RUN: execution plan and evidence.\n\n## Verification\n- `python atlas.py doctor`\n- (project tests as defined)\n""",
    ATLAS_ROOT / "GOALS.md": """# GOALS\n\n- Purpose: (fill in)\n- In scope: (fill in)\n- Out of scope: (fill in)\n""",
}

DEFAULT_TEMPLATES = {
    "REQ.md": """# [REQ-XXX-001] Title\n\n> **ID**: REQ-XXX-001\n> **Domain**: XXX\n> **Status**: Draft\n> **Last Updated**: YYYY-MM-DD\n> **Must-Read**: RULE-XXX-001\n\n---\n\n## Decision\n- (what must be true)\n\n## Input\n- (inputs)\n\n## Output\n- (outputs)\n\n## Acceptance Criteria\n- [ ] (criteria)\n""",
    "RULE.md": """# [RULE-XXX-001] Title\n\n> **ID**: RULE-XXX-001\n> **Domain**: XXX\n> **Priority**: Medium\n> **Last Updated**: YYYY-MM-DD\n> **Must-Read**: RULE-XXX-001\n\n---\n\n## Rule Statement\n- (always true / forbidden)\n\n## Scope\n- (where it applies)\n\n## Violation\n- (what counts as a violation)\n\n## Examples\n\n### Correct\n- (example)\n\n### Incorrect\n- (example)\n""",
    "CQ.md": """# [CQ-XXX-001] Title\n\n> **ID**: CQ-XXX-001\n> **Domain**: XXX\n> **Status**: Draft\n> **Last Updated**: YYYY-MM-DD\n\n---\n\n## Question\n- (what must the system answer?)\n\n## Expected Answer (Criteria)\n1. ...\n2. ...\n\n## Traceability\n- **Solves by**: [REQ-XXX-001](../req/REQ-XXX-001.md)\n- **Constrained by**: [RULE-XXX-001](../rule/RULE-XXX-001.md)\n""",
    "BRIEF.md": """# [BRIEF-XXX-001] Title\n\n> **ID**: BRIEF-XXX-001\n> **Domain**: XXX\n> **Status**: Active\n> **Date**: YYYY-MM-DD\n\n## 1. User Request\n- (raw text)\n\n## 2. Intent Summary\n- Goal:\n- Problem:\n\n## 3. Affected Artifacts\n- Create: \n- Modify: \n- Read: \n\n## 4. Proposed Changes\n1. \n2. \n\n## 5. Verification Criteria\n- [ ] \n""",
    "RUN.md": """# [RUN-BRIEF-XXX-001-step-01] Title\n\n> **ID**: RUN-BRIEF-XXX-001-step-01\n> **Brief**: BRIEF-XXX-001\n> **Status**: Planned\n> **Started**: YYYY-MM-DD\n> **Git**: -\n> **Completed**: -\n\n## Input\n- (documents to read)\n\n## Steps\n- [ ] \n\n## Verification\n- [ ] Test\n- [ ] Spec\n- [ ] Boundary\n\n## Output\n- (files created/modified)\n""",
}

DEFAULT_PROMPTS = {
    "onboarding.md": """# Atlas Audit Prompt

> **Note**: 기존 `Onboarding Prompt`가 **`Audit Prompt`**로 재정의되었습니다.
> 이 프롬프트는 더 이상 파일을 자동으로 생성하지 않으며, 현재 프로젝트와 문서 간의 **정합성(Consistency)을 감사(Audit)**하는 역할을 수행합니다.

---

## Prompt

```
당신은 이 프로젝트의 **문서 정합성 감사관(Auditor)**입니다.
이미 존재하는 Atlas 문서들(.atlas/ 폴더 내 GOALS, CONVENTIONS, BOARD, FRONT)이 현재 프로젝트의 실제 상태(코드, 최근 작업, 기술 스택 등)와 일치하는지 점검하는 것이 주 임무입니다.

### [Strict Rules] 핵심 규칙
1. **READ-ONLY**: 절대, 어떤 경우에도 기존 파일을 직접 수정하거나 내용을 자동 업데이트하지 마세요.
2. **제안 모드 (Suggestion Only)**: 불일치나 누락이 발견되면 "어떻게 수정하면 좋을지"를 제안 형식으로만 출력하세요.
3. **비판적 시각**: 단순히 내용을 요약하지 말고, "정말 이 내용이 현재 유효한가?"를 끊임없이 의심하며 검증하세요.

### [Checklist] 검사 관점

LLM은 다음 기준에 따라 각 문서를 엄격하게 평가해야 합니다:

#### 1. GOALS.md (목표 정합성)
- **Active Task와 일치 여부**: 현재 진행 중인 작업들이 GOALS에 정의된 핵심 목표를 벗어나지 않았는가?
- **Scope Creep 감지**: 최근 논의되거나 추가된 기능이 In-Scope 범위 내에 있는가? 아니면 범위를 조용히 넓히고 있는가?

#### 2. CONVENTIONS.md (규칙 현실성)
- **위반 가능성 점검**: 실제 코드나 최근 커밋 내용이 문서의 규칙(Always, Never)을 위반하고 있지 않은가?
- **구체성 검증**: 규칙이 너무 추상적이어서(예: "깨끗한 코드 작성") 실제 지침이 되지 못하는 부분은 없는가?

#### 3. BOARD.md (현황 동기화)
- **Active 상태 검증**: Active에 있는 작업이 현재 실제로 진행 중인가? (GOALS 범위를 벗어난 작업이 Active에 있는가?)
- **Queue 방치 점검**: Queue에 있는 항목들이 너무 오래 방치되어, 현재의 GOALS와 맞지 않게 되었는가?

#### 4. FRONT.md (환경 최신화)
- **기술 스택 현실화**: 문서에 적힌 기술 스택이 실제 프로젝트 코드와 일치하는가?
- **암묵적 전제**: 팀 내에서 암묵적으로 합의된 중요한 변경 사항이 문서에서 누락되지 않았는가?

---

### [Audit Report] 출력 양식

각 파일별로 아래 상태 아이콘을 사용하여 진단 결과를 출력하세요.

- [PASS] **일치 (Pass)**
- [WARN] **의심 (Warning)**: 확인이 필요하거나 모호한 부분.
- [FAIL] **불일치/누락 (Fail)**: 명확한 오류, 즉시 수정 필요.

**[작성 예시]**

### 1. GOALS.md
- [PASS] 핵심 목표 여전히 유효함.
- [WARN] **의심**: '실시간 채팅' 기능이 최근 작업(Task-102)에서 구현 중인데, GOALS의 Scope에는 명시되지 않았음. 업데이트 필요.

### 2. CONVENTIONS.md
- [FAIL] **불일치**: 문서에는 'Type Hint 필수'라고 되어 있으나, 최근 `utils.py` 등에서 많은 함수가 타이핑 없이 작성됨.
    - **제안**: 규칙을 강화하거나, 예외 상황을 문서에 명시할 것.

(이하 BOARD, FRONT 동일 포맷)
```

---

## How to execute
이 프롬프트는 정기적으로(또는 프로젝트 방향성이 흔들릴 때) LLM에게 제시하여 문서 부채를 점검하는 용도로 사용합니다.
""",
}


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


def load_default_top_docs() -> dict[Path, str]:
    docs = dict(DEFAULT_TOP_DOCS)
    if SRC_DEFAULT_TOP_DOCS_DIR.is_dir():
        for path in sorted(SRC_DEFAULT_TOP_DOCS_DIR.glob("*.md")):
            target = ATLAS_ROOT / path.name
            if target in docs:
                docs[target] = read_text(path)
    return docs


def load_default_templates() -> dict[str, str]:
    templates = dict(DEFAULT_TEMPLATES)
    if SRC_DEFAULT_TEMPLATES_DIR.is_dir():
        for name in DEFAULT_TEMPLATES:
            src_path = SRC_DEFAULT_TEMPLATES_DIR / name
            if src_path.exists():
                templates[name] = read_text(src_path)
    return templates


def load_default_prompts() -> dict[str, str]:
    prompts = dict(DEFAULT_PROMPTS)
    if SRC_DEFAULT_PROMPTS_DIR.is_dir():
        for name in DEFAULT_PROMPTS:
            src_path = SRC_DEFAULT_PROMPTS_DIR / name
            if src_path.exists():
                prompts[name] = read_text(src_path)
    return prompts


def load_default_system_files() -> dict[str, str]:
    """Load VERSION and VERSIONING.md from src/.system_defaults/."""
    files: dict[str, str] = {}
    for name in ["VERSION", "VERSIONING.md"]:
        src_path = SRC_DEFAULTS_ROOT / name
        if src_path.exists():
            files[name] = read_text(src_path)
    return files


def load_default_src_files() -> dict[str, str]:
    """Load source files - either from defaults dir or embedded in atlas.py."""
    files: dict[str, str] = {}
    
    # Try loading from src/.system_defaults/src/ first (development mode)
    src_dir = SRC_DEFAULTS_ROOT / "src"
    if src_dir.is_dir():
        for path in src_dir.glob("*.py"):
            files[path.name] = read_text(path)
    
    # If no files found and running as bundled atlas.py, embed self
    if not files:
        # When running as atlas.py, include self as the source
        _self_path = Path(__file__).resolve()
        if _self_path.name == "atlas.py" or _self_path.name != "atlas_cli.py":
            # Read the current file content (which contains all the code)
            try:
                files["atlas_cli.py"] = read_text(_self_path)
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
    return re.findall(r"(?:REQ|RULE|CQ|BRIEF|RUN)-[A-Z]+-\d{3}(?:-step-\d{2})?", text)


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
    for d in [REQ_DIR, RULE_DIR, CQ_DIR, BRIEF_DIR, RUN_DIR, IDEA_DIR, TEMPLATES_DIR, STATE_DIR, SYSTEM_ROOT / "prompts", SYSTEM_ROOT / "src"]:
        ensure_dir(d)

    for path, content in load_default_top_docs().items():
        if overwrite or not path.exists():
            write_text(path, content)

    for name, content in load_default_templates().items():
        template_path = TEMPLATES_DIR / name
        if overwrite or not template_path.exists():
            write_text(template_path, content)

    prompts_dir = SYSTEM_ROOT / "prompts"
    for name, content in load_default_prompts().items():
        prompt_path = prompts_dir / name
        if overwrite or not prompt_path.exists():
            write_text(prompt_path, content)
            print(f"[OK] Created {prompt_path}")

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


def intake_command(args: argparse.Namespace) -> int:
    domain = args.domain.upper()
    brief_id = next_id("BRIEF", domain, BRIEF_DIR, BRIEF_ID_PATTERN)

    title_src = " ".join(args.text.strip().splitlines()).strip()
    title = title_src[:60] + ("..." if len(title_src) > 60 else "")
    if not title:
        title = "User Request"

    content = f"""# [{brief_id}] {title}

> **ID**: {brief_id}
> **Domain**: {domain}
> **Status**: Active
> **Date**: {now_date()}

## 1. User Request
{args.text.strip()}

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
    write_text(path, content)
    print(f"[OK] Created {path}")
    return 0


def create_req_stub(req_id: str) -> None:
    path = REQ_DIR / f"{req_id}.md"
    if path.exists():
        return
    match = REQ_ID_PATTERN.match(req_id)
    if not match:
        return
    domain = match.group(1)
    template = load_template("REQ.md")
    content = (
        template.replace("REQ-XXX-001", req_id)
        .replace("Domain**: XXX", f"Domain**: {domain}")
        .replace("Last Updated**: YYYY-MM-DD", f"Last Updated**: {now_date()}")
    )
    write_text(path, content)


def plan_command(args: argparse.Namespace) -> int:
    brief_id = args.brief_id
    if brief_id.endswith(".md"):
        brief_id = Path(brief_id).stem

    match = BRIEF_ID_PATTERN.match(brief_id)
    if not match:
        print(f"[ERR] Invalid BRIEF ID: {brief_id}")
        return 1

    brief_path = BRIEF_DIR / f"{brief_id}.md"
    if not brief_path.exists():
        print(f"[ERR] BRIEF not found: {brief_path}")
        return 1

    domain = match.group(1)
    number = match.group(2)
    run_id = f"RUN-BRIEF-{domain}-{number}-step-01"
    run_path = RUN_DIR / f"{run_id}.md"
    if run_path.exists():
        print(f"[ERR] RUN already exists: {run_path}")
        return 1

    brief_text = read_text(brief_path)
    artifacts = parse_affected_artifacts(brief_text)
    req_ids = [
        rid
        for rid in extract_ids_from_text(" ".join(artifacts["Create"] + artifacts["Modify"]))
        if rid.startswith("REQ-")
    ]
    for req_id in req_ids:
        create_req_stub(req_id)

    input_lines = [f"- {brief_id}"]
    for req_id in req_ids:
        input_lines.append(f"- {req_id}")

    content = f"""# [{run_id}] Plan

> **ID**: {run_id}
> **Brief**: {brief_id}
> **Status**: Planned
> **Started**: {now_date()}
> **Git**: -
> **Completed**: -

## Input
{os.linesep.join(input_lines)}

## Steps
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
            "brief_id": brief_id,
            "stage": "executing",
            "updated_at": now_iso(),
        }
    )

    print(f"[OK] Created {run_path}")
    return 0


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

    text = read_text(run_path)
    meta = extract_meta(text)
    brief_id = meta.get("Brief")
    status = "Completed" if args.success else "Failed"
    text = update_meta_line(text, "Status", status)
    text = update_meta_line(text, "Git", args.git)
    text = update_meta_line(text, "Completed", now_date())
    write_text(run_path, text)

    if brief_id:
        update_brief_status(brief_id, status)

    last_run_state = {
        "run_id": run_id,
        "stage": "finished",
        "git_hash": args.git,
        "completed_at": now_iso(),
    }
    if brief_id:
        last_run_state["brief_id"] = brief_id
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

    required_dirs = [REQ_DIR, RULE_DIR, CQ_DIR, BRIEF_DIR, RUN_DIR, SYSTEM_ROOT, TEMPLATES_DIR, STATE_DIR]
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

    scan_dirs = [REQ_DIR, RULE_DIR, CQ_DIR, BRIEF_DIR, RUN_DIR]
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

    intake = sub.add_parser("intake")
    intake.add_argument("text")
    intake.add_argument("--domain", default="GEN")

    plan = sub.add_parser("plan")
    plan.add_argument("brief_id")

    finish = sub.add_parser("finish")
    finish.add_argument("run_id")
    finish.add_argument("--git", required=True)
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

    if args.command == "init":
        return init_command(args)
    if args.command == "intake":
        return intake_command(args)
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
