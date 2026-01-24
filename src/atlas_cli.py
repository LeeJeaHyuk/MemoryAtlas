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

DEFAULT_TOP_DOCS = {
    ATLAS_ROOT / "FRONT.md": """# Atlas\n\nThis repo uses Atlas vNext.\nUse: `python atlas.py init`\n\nQuick flow:\n1) `python atlas.py intake \"...\" --domain GEN`\n2) `python atlas.py plan BRIEF-GEN-001`\n3) `python atlas.py finish RUN-BRIEF-GEN-001-step-01 --git <hash|no-commit> --success true`\n\nLinks: BOARD.md, CONVENTIONS.md, GOALS.md\n""",
    ATLAS_ROOT / "BOARD.md": """# BOARD\n\n## Queue\n- (empty)\n\n## Active\n- (empty)\n\n## Done\n- (empty)\n""",
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
    "onboarding.md": "# Atlas Onboarding Prompt\n\n이 프롬프트를 Claude에게 전달하여 프로젝트 초기 설정을 완료하세요.\n\n---\n\n## Prompt\n\n```\n이 프로젝트에 Atlas 문서 시스템이 설치되었습니다.\n.atlas/ 폴더의 GOALS.md, CONVENTIONS.md, BOARD.md, FRONT.md를 프로젝트에 맞게 설정해주세요.\n\n다음 질문에 답변해주세요:\n\n1. **프로젝트 목적** (GOALS.md용)\n   - 이 프로젝트의 핵심 목표는 무엇인가요?\n   - 범위 내(In scope)와 범위 외(Out of scope)를 구분해주세요.\n\n2. **작업 규칙** (CONVENTIONS.md용)\n   - 항상 지켜야 할 규칙은? (Always)\n   - 먼저 물어봐야 할 것은? (Ask First)\n   - 절대 하면 안 되는 것은? (Never)\n\n3. **현재 작업 상태** (BOARD.md용)\n   - 대기 중인 작업은? (Queue)\n   - 진행 중인 작업은? (Active)\n\n4. **추가 컨텍스트** (FRONT.md용)\n   - 이 프로젝트의 기술 스택은?\n   - 특별히 알아야 할 것이 있나요?\n\n답변을 받으면 해당 파일들을 자동으로 업데이트하겠습니다.\n```\n\n---\n\n## After Onboarding\n\n설정 완료 후: `python atlas.py doctor` 실행하여 검증\n",
}


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


def extract_ids_from_text(text: str) -> list[str]:
    return re.findall(r"(?:REQ|RULE|CQ|BRIEF|RUN)-[A-Z]+-\d{3}(?:-step-\d{2})?", text)


def write_last_run(state: dict) -> None:
    ensure_dir(STATE_DIR)
    write_text(LAST_RUN_PATH, json.dumps(state, indent=2) + "\n")


def init_command(_args: argparse.Namespace) -> int:
    ensure_dir(ATLAS_ROOT)
    for d in [REQ_DIR, RULE_DIR, CQ_DIR, BRIEF_DIR, RUN_DIR, IDEA_DIR, TEMPLATES_DIR, STATE_DIR, SYSTEM_ROOT / "prompts"]:
        ensure_dir(d)

    for path, content in DEFAULT_TOP_DOCS.items():
        if not path.exists():
            write_text(path, content)

    for name, content in DEFAULT_TEMPLATES.items():
        template_path = TEMPLATES_DIR / name
        if not template_path.exists():
            write_text(template_path, content)

    prompts_dir = SYSTEM_ROOT / "prompts"
    for name, content in DEFAULT_PROMPTS.items():
        prompt_path = prompts_dir / name
        if not prompt_path.exists():
            write_text(prompt_path, content)
            print(f"[OK] Created {prompt_path}")

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
    status = "Completed" if args.success else "Failed"
    text = update_meta_line(text, "Status", status)
    text = update_meta_line(text, "Git", args.git)
    text = update_meta_line(text, "Completed", now_date())
    write_text(run_path, text)

    write_last_run(
        {
            "run_id": run_id,
            "stage": "finished",
            "git_hash": args.git,
            "completed_at": now_iso(),
        }
    )

    print(f"[OK] Updated {run_path}")
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
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init")

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

    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

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

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
