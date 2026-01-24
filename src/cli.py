#!/usr/bin/env python3
"""
MemoryAtlas v2.4.0 - Memory-Driven Development Tool (Context Bootstrapping)

=== VERSION HISTORY ===

v2.0.0: Initial What-How-Log structure
v2.1.0: Bug fixes, --doctor, template versioning
v2.1.1: **ID**: as authority, three-way validation

v2.2.0 - Authority Separation & Execution Unit:
1. REQ split into 3 layers: DECISION (authority) / DISCUSSION / RATIONALE
2. Must-Read field enforced in all REQ documents
3. Execution documents split into small units (RUN-*)
4. New folder structure: discussions/, rationale/
5. Validation for Must-Read links
6. RUN document format enforcement

v2.2.1 - P0/P1 Fixes:
  - Fixed header regex to support H1 (#) in addition to H2/H3
  - Fixed Must-Read existence check to use regex instead of string contains
  - Added ADR existence validation (no longer skipped)
  - Expanded LINT_DIRS to include discussions and active RUNs
  - Added 3-way ID consistency check for RUN documents
  - Improved Must-Read parsing to return clean IDs (no links)

v2.3.0 - Smart Spec Edition:
  - CONVENTIONS rewritten with 6 core sections + Boundaries
  - Added Commands section for explicit test/lint/run commands
  - Added Boundaries (Always/Ask First/Never) for AI behavior control
  - REQ template updated with optional Constraints & Boundaries section
  - RUN template updated with Self-Check verification checklist
  - AGENT_RULES updated to enforce Boundaries compliance
  - Enhanced AI predictability through explicit behavioral rules

v2.5.0 (Current) - Reverse Engineering & Context Bootstrapping:
  - Added --reverse mode for partial code analysis (Reverse Engineering)
  - Added --focus argument for targeted analysis
  - Context Bootstrapping (v2.4) features included
  - "LLM이 관리할 폴더를 LLM이 초기화" 철학 강화

=== SMART SPEC MODEL ===

6 Core Sections in CONVENTIONS:
  1. Commands: Test, Lint, Run commands
  2. Project Structure: Directory layout
  3. Code Style: Formatting, naming conventions
  4. Testing Strategy: Test requirements
  5. Git Workflow: Branch/commit conventions
  6. Boundaries: Always / Ask First / Never rules

Boundaries (STRICT):
  ✅ Always: Actions AI must always perform
  ⚠️ Ask First: Actions requiring human approval
  🚫 Never: Actions AI must never perform

=== AUTHORITY MODEL ===

권위의 흐름 (Authority Flow):
  REQ (Authority) → TECH_SPEC → CODE → RUN/LOG

문서 등급 (Document Grades):
  - DECISION (Authority): 최종 결정만. 짧고 단단하게.
  - DISCUSSION: 사람-AI 조율 기록. LLM은 기본적으로 안 읽음.
  - RATIONALE/ADR: 왜 그렇게 결정했는지. 필요 시만.
  - EXECUTION (RUN): 작업 단위. 1목적 + 1검증 + 1결과.

=== EXECUTION UNIT ===

실행 문서 = 1개의 목적 + 1개의 검증 방법 + 1개의 결과
- RUN-REQ-AUTH-001-step-01.md
- RUN-REQ-AUTH-001-step-02.md
- ...

실행 문서 구조:
- Input: 읽을 문서 ID 목록 (P0 + Must-Read)
- Steps: 명령/행동
- Verification: 성공 조건 + Self-Check
- Output: 생성/수정 파일 목록
"""

import argparse
import sys
from pathlib import Path

from core.bootstrap import bootstrap_init
from core.bootstrap_mcp import bootstrap_mcp
from core.checks import (
    check_links,
    check_requirements,
    check_runs,
    check_structure,
    check_mcp,
    doctor,
    lint_metadata,
)
from core.automation import Automator
from core.config import CURRENT_VERSION, ROOT_DIR
from core.status import status_report, list_runs
from core.update import init_or_update
from core.reverse import generate_reverse_prompt
from utils.fs import ensure_structure, update_onboarding_guide, update_onboarding_prompt

def parse_args() -> "argparse.Namespace":
    parser = argparse.ArgumentParser(
        description=f"MemoryAtlas v{CURRENT_VERSION} - Memory-Driven Development Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python memory_manager.py              # Initialize/update system
  python memory_manager.py --doctor     # Run all checks
  python memory_manager.py --status     # Show task summary
  python memory_manager.py --guide      # Show onboarding guide and prompt
  python memory_manager.py --refresh-guide  # Regenerate onboarding guide from state
  python memory_manager.py --dry-run    # Preview changes
        """
    )

    parser.add_argument(
        "command",
        nargs="?",
        choices=["apply-req"],
        help="Optional automation command (apply-req).",
    )
    parser.add_argument(
        "--id",
        dest="command_req_id",
        help="REQ ID for automation commands such as apply-req.",
    )
    parser.add_argument(
        "--no-spec",
        action="store_true",
        help="Skip spec draft creation when running apply-req.",
    )

    update_group = parser.add_argument_group("Update Commands")
    update_group.add_argument(
        "--migrate",
        action="store_true",
        help="Force migration from v1.x to v2.x structure.",
    )
    update_group.add_argument(
        "--update",
        action="store_true",
        help="Run init/update even when using checks.",
    )
    update_group.add_argument(
        "--bootstrap",
        action="store_true",
        help="Create BOOTSTRAP_PROMPT.md for AI-driven project initialization (Context Bootstrapping).",
    )
    update_group.add_argument(
        "--bootstrap-mcp",
        action="store_true",
        help="Create MCP bootstrap prompt and templates for a target client.",
    )
    update_group.add_argument(
        "--reverse",
        action="store_true",
        help="Generate reverse engineering prompt for partial code analysis.",
    )
    update_group.add_argument(
        "--guide",
        action="store_true",
        help="Show onboarding guide location and output LLM prompt for interactive setup.",
    )
    update_group.add_argument(
        "--refresh-guide",
        action="store_true",
        help="Regenerate onboarding guide from state without full update.",
    )
    update_group.add_argument(
        "--focus",
        type=str,
        help="Focus path for reverse engineering (e.g., src/auth).",
    )
    update_group.add_argument(
        "--target",
        type=str,
        help="Target client for bootstrap-mcp or mcp-check (claude_code, claude_desktop, codex, gemini_cli, ci).",
    )
    update_group.add_argument(
        "--os",
        dest="os_name",
        type=str,
        choices=["windows", "unix"],
        help="Target OS for bootstrap-mcp (windows or unix).",
    )

    check_group = parser.add_argument_group("Check Commands")
    check_group.add_argument(
        "--doctor",
        action="store_true",
        help="Run all checks (structure, lint, links, requirements, runs).",
    )
    check_group.add_argument(
        "--check",
        action="store_true",
        help="Validate structure and required files.",
    )
    check_group.add_argument(
        "--lint",
        action="store_true",
        help="Check metadata headers in key documents.",
    )
    check_group.add_argument(
        "--links",
        action="store_true",
        help="Validate links in .memory docs.",
    )
    check_group.add_argument(
        "--allow-absolute-links",
        action="store_true",
        help="Allow absolute paths in links (not recommended).",
    )
    check_group.add_argument(
        "--req",
        action="store_true",
        help="Validate requirement documents (authority model).",
    )
    check_group.add_argument(
        "--runs",
        action="store_true",
        help="Validate RUN documents (execution unit model).",
    )
    check_group.add_argument(
        "--mcp-check",
        action="store_true",
        help="Validate MCP bootstrap outputs (templates and scripts).",
    )

    status_group = parser.add_argument_group("Status Commands")
    status_group.add_argument(
        "--status",
        action="store_true",
        help="Show status report of tasks and knowledge.",
    )
    status_group.add_argument(
        "--recent",
        type=int,
        default=5,
        metavar="N",
        help="Number of recent active tasks to show (default: 5).",
    )
    status_group.add_argument(
        "--list-runs",
        nargs="?",
        const="all",
        metavar="STATUS",
        help="List RUN documents. Filter by status: active, completed, failed, all (default: all).",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without writing.",
    )

    return parser.parse_args()

def main() -> int:
    args = parse_args()

    if args.command == "apply-req":
        req_id = args.command_req_id
        if not req_id:
            print("Error: --id is required when running apply-req")
            return 1
        automator = Automator()
        report = automator.apply_req(
            req_id, dry_run=args.dry_run, create_spec=not args.no_spec
        )
        if report["status"] == "failed":
            print("apply-req failed:")
            for err in report["errors"]:
                print(f"  - {err}")
            if report["disc"]:
                print(f"  DISC created: {report['disc']}")
            return 1
        print(f"apply-req {report['status']}:")
        for name, path in report["artifacts"].items():
            print(f"  {name}: {path}")
        return 0

    if args.bootstrap_mcp:
        if not args.target or not args.os_name:
            print("Error: --target and --os are required when running --bootstrap-mcp")
            return 1
        bootstrap_mcp(args.target, args.os_name, dry_run=args.dry_run)
        return 0

    # Bootstrap mode: create AI kick-off meeting files and exit
    if args.bootstrap:
        bootstrap_init(dry_run=args.dry_run)
        return 0

    if args.reverse:
        if not args.focus:
            print("Error: --focus is required when using --reverse (e.g., --focus src/core)")
            return 1
        generate_reverse_prompt(ROOT_DIR, args.focus)
        return 0

    if args.guide:
        init_or_update(dry_run=args.dry_run, force_migrate=args.migrate)

        memory_root = Path(ROOT_DIR)
        guide_path = memory_root / "GETTING_STARTED.md"
        prompt_path = memory_root / "00_SYSTEM" / "ONBOARDING_PROMPT.md"

        print("\n" + "=" * 60)
        print("🚀 MemoryAtlas 온보딩 가이드")
        print("=" * 60 + "\n")

        print("📖 가이드 문서 위치:")
        print(f"   - 사용자 가이드: {guide_path}")
        print(f"   - 온보딩 프롬프트: {prompt_path}\n")

        missing = []
        if not guide_path.exists():
            missing.append(str(guide_path))
        if not prompt_path.exists():
            missing.append(str(prompt_path))

        if missing:
            print("⚠️  온보딩 파일이 없습니다:")
            for item in missing:
                print(f"   - {item}")
            if args.dry_run:
                print("    --dry-run 모드라 파일이 생성되지 않았습니다.")
                print("    다시 실행: python memory_manager.py --guide")
            else:
                print("    먼저 'python memory_manager.py'를 실행하여 .memory 폴더를 생성하세요.")
            return 1

        print("=" * 60)
        print("📋 아래 프롬프트를 LLM에게 전달하세요:")
        print("=" * 60 + "\n")
        print(prompt_path.read_text(encoding="utf-8"))
        return 0

    if args.refresh_guide:
        ensure_structure(ROOT_DIR)
        update_onboarding_prompt(ROOT_DIR, dry_run=args.dry_run)
        update_onboarding_guide(ROOT_DIR, dry_run=args.dry_run, force=True)
        return 0

    run_checks = any([
        args.doctor,
        args.check,
        args.lint,
        args.links,
        args.req,
        args.runs,
        args.mcp_check,
        args.status,
    ])
    run_update = args.update or args.migrate or not run_checks

    exit_code = 0

    if run_update:
        init_or_update(dry_run=args.dry_run, force_migrate=args.migrate)

    if args.doctor:
        exit_code = doctor(ROOT_DIR, allow_absolute_links=args.allow_absolute_links)
    else:
        if args.check:
            exit_code += check_structure(ROOT_DIR)
        if args.lint:
            exit_code += lint_metadata(ROOT_DIR)
        if args.links:
            exit_code += check_links(ROOT_DIR, allow_absolute=args.allow_absolute_links)
        if args.req:
            exit_code += check_requirements(ROOT_DIR)
        if args.runs:
            exit_code += check_runs(ROOT_DIR)
        if args.mcp_check:
            exit_code += check_mcp(ROOT_DIR, target=args.target)

    if args.status:
        status_report(ROOT_DIR, show_recent=args.recent)

    if args.list_runs:
        list_runs(ROOT_DIR, status_filter=args.list_runs)

    return exit_code


if __name__ == "__main__":
    sys.exit(main())

