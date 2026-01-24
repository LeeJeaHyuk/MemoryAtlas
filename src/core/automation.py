from __future__ import annotations

import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from core.config import REQ_ID_PATTERN, ROOT_DIR, TEMPLATE_VERSION

META_RE = re.compile(r"> \*\*(.+?)\*\*:\s*(.+)")
AFFECTED_LINE_RE = re.compile(r"^\s*-\s*\*{0,2}(Modify|Create|Delete|Read)\*{0,2}\s*:\s*(.+)$", re.I)
MD_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")



class Automator:
    """Automation engine for MCP pipelines."""

    def __init__(self, root: Optional[str] = None):
        self.root = Path(root or ROOT_DIR)
        self.req_dir = self.root / "02_REQUIREMENTS" / "capabilities"
        self.spec_dir = self.root / "03_TECH_SPECS" / "architecture"
        self.run_dir = self.root / "04_TASK_LOGS" / "active"
        self.archive_dir = self.root / "04_TASK_LOGS" / "archive"
        self.disc_dir = self.root / "02_REQUIREMENTS" / "discussions"
        self.brief_dir = self.disc_dir / "briefs"
        self.last_error: Optional[str] = None

    def _req_path(self, req_id: str) -> Path:
        return self.req_dir / f"{req_id}.md"

    def _parse_metadata(self, text: str) -> Dict[str, str]:
        metadata: Dict[str, str] = {}
        for line in text.splitlines():
            match = META_RE.match(line.strip())
            if not match:
                continue
            key, value = match.groups()
            metadata[key] = value.strip()
        return metadata

    def _req_parts(self, req_id: str) -> Optional[Dict[str, str]]:
        match = REQ_ID_PATTERN.match(req_id)
        if not match:
            return None
        domain, index = match.groups()
        return {"domain": domain, "index": index}

    def _format_run_id(self, req_id: str) -> str:
        parts = self._req_parts(req_id)
        if not parts:
            return f"RUN-{req_id}-step-01"
        return f"RUN-REQ-{parts['domain']}-{parts['index']}-step-01"

    def _now_date(self) -> str:
        return datetime.utcnow().date().isoformat()

    def _parse_bool(self, value: Optional[str]) -> bool:
        if value is None:
            return False
        return value.strip().lower() in {"true", "yes", "1", "y"}

    def _requires_spec(self, req_id: str) -> bool:
        metadata = self._parse_metadata(self._req_path(req_id).read_text(encoding="utf-8"))
        return self._parse_bool(metadata.get("Requires-Spec"))

    def _update_meta_line(self, text: str, key: str, value: str) -> str:
        pattern = re.compile(rf"^>\s*\*\*{re.escape(key)}\*\*:\s*.*$", re.MULTILINE)
        line = f"> **{key}**: {value}"
        if pattern.search(text):
            return pattern.sub(line, text)
        lines = text.splitlines()
        insertion = None
        for i, ln in enumerate(lines):
            if ln.strip().startswith("> **"):
                insertion = i + 1
                break
        if insertion is not None:
            lines.insert(insertion, line)
            return "\n".join(lines)
        return line + "\n" + text

    def validate_req(self, req_id: str) -> bool:
        report = self.req_status(req_id)
        self.last_error = "; ".join(report["blocking_issues"]) if not report["readiness"] else None
        return report["readiness"]

    def req_status(self, req_id: str) -> Dict[str, Any]:
        """Inspect REQ readiness without executing pipeline."""
        issues = []
        metadata: Dict[str, str] = {}
        path = self._req_path(req_id)
        if not path.exists():
            issues.append(f"REQ not found: {req_id}")
            return {
                "status": None,
                "metadata": {},
                "readiness": False,
                "blocking_issues": issues,
            }
        if not self._req_parts(req_id):
            issues.append(f"Invalid REQ ID format: {req_id}")
        metadata = self._parse_metadata(path.read_text(encoding="utf-8"))
        status = metadata.get("Status", "")
        if status.lower() != "active":
            issues.append(f"REQ is not Active (status={status or 'missing'})")
        readiness = len(issues) == 0
        return {
            "status": status or None,
            "metadata": metadata,
            "readiness": readiness,
            "blocking_issues": issues,
        }

    def _spec_content(self, req_id: str) -> str:
        metadata = self._parse_metadata(self._req_path(req_id).read_text(encoding="utf-8"))
        title = metadata.get("Title", req_id)
        return (
            f"# [SPEC-{req_id}] {title} Implementation\n\n"
            f"> **ID**: SPEC-{req_id}\n"
            f"> **Related-REQ**: {req_id}\n"
            "> **Status**: Draft\n"
            f"> **Template-Version**: {TEMPLATE_VERSION}\n\n"
            "## Purpose\n"
            f"This spec captures how we intend to implement {req_id}.\n\n"
            "## Design Summary\n"
            " - TODO: capture key decisions\n\n"
            "## Verification\n"
            " - RUN document covers the validation gates.\n"
        )

    def create_spec_draft(self, req_id: str, dry_run: bool = False) -> Path:
        """Create a lightweight spec draft in 03_TECH_SPECS/architecture."""
        req_path = self._req_path(req_id)
        if not req_path.exists():
            raise FileNotFoundError(f"REQ missing: {req_id}")
        self.spec_dir.mkdir(parents=True, exist_ok=True)
        spec_path = self.spec_dir / f"SPEC-{req_id}.md"
        if dry_run:
            return spec_path
        spec_path.write_text(self._spec_content(req_id), encoding="utf-8")
        return spec_path

    def _run_content(self, run_id: str, req_id: str, spec_ref: str) -> str:
        return (
            f"# [{run_id}] Implement {req_id}\n\n"
            f"> **ID**: {run_id}\n"
            "> **Status**: Active\n"
            f"> **Started**: {self._now_date()}\n"
            f"> **Input**: {req_id}\n"
            "> **Verification**: apply_req pipeline\n"
            f"> **Template-Version**: {TEMPLATE_VERSION}\n\n"
            "## Objective (목표)\n"
            "Deliver the change described in the authority document.\n\n"
            "## Scope (범위)\n"
            "### In Scope\n"
            "- Implementation and validation steps referenced from the REQ.\n\n"
            "### Out of Scope\n"
            "- Anything not already described in the authority doc.\n\n"
            "## Steps (단계)\n"
            "1. Analyze current code.\n"
            "2. Implement the requested behavior.\n"
            "3. Run validation gates (`python memory_manager.py --doctor`).\n\n"
            "## Verification (Self-Check)\n"
            "- [ ] Tests\n"
            "- [ ] Boundaries\n"
            "- [ ] Spec reference\n\n"
            "## Output (결과물)\n"
            f"- RUN references spec draft: {spec_ref}\n"
        )

    def create_run(
        self, req_id: str, spec_path: Optional[Path] = None, dry_run: bool = False
    ) -> Path:
        """Create a RUN in 04_TASK_LOGS/active matching the REQ."""
        self.run_dir.mkdir(parents=True, exist_ok=True)
        run_id = self._format_run_id(req_id)
        run_path = self.run_dir / f"{run_id}.md"
        spec_ref = spec_path.name if spec_path else "n/a"
        if dry_run:
            return run_path
        run_path.write_text(self._run_content(run_id, req_id, spec_ref), encoding="utf-8")
        return run_path

    def finalize_run(self, run_id: str, success: bool = True, git_hash: str = "") -> Path:
        """Update RUN status and record evidence. RUN remains in active (no archive move).

        Args:
            run_id: The RUN document ID
            success: Whether the run was successful
            git_hash: Git commit hash as evidence (optional, can be 'no-commit')

        Returns:
            Path to the updated RUN document (stays in active/)
        """
        source = self.run_dir / f"{run_id}.md"
        if not source.exists():
            raise FileNotFoundError(f"RUN not found: {run_id}")
        text = source.read_text(encoding="utf-8")

        # Update metadata
        text = self._update_meta_line(text, "Status", "Completed" if success else "Failed")
        text = self._update_meta_line(text, "Completed", self._now_date())
        if git_hash:
            text = self._update_meta_line(text, "Git", git_hash)

        # Add result note
        note = "\n## Result\n"
        note += "Success\n" if success else "Failure - requires follow-up\n"
        if git_hash:
            note += f"\n**Git Evidence**: `{git_hash}`\n"

        source.write_text(text + note, encoding="utf-8")

        # No archive move - RUN stays in active/
        return source

    def create_disc_from_failure(self, target_id: str, error_log: str) -> Path:
        """Create a DISC entry describing the failure."""
        self.disc_dir.mkdir(parents=True, exist_ok=True)
        domain = target_id.split("-")[1] if "-" in target_id else "GEN"
        suffix = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        disc_id = f"DISC-{domain}-{suffix}"
        disc_path = self.disc_dir / f"{disc_id}.md"
        content = (
            f"# [{disc_id}] Automated failure for {target_id}\n\n"
            f"> **ID**: {disc_id}\n"
            f"> **Related-REQ**: {target_id}\n"
            f"> **Date**: {self._now_date()}\n\n"
            "## Summary\n"
            "Automated pipeline encountered a failure.\n\n"
            "## Evidence\n"
            f"```\n{error_log}\n```\n\n"
            "## Hypotheses\n"
            "1. Required metadata missing.\n"
            "2. Run template could not be created due to permissions.\n\n"
            "## Fix Options\n"
            "- Correct metadata and rerun.\n"
            "- Clear the active RUN and retry.\n\n"
            "## Next Steps\n"
            "- Review the log.\n"
            "- Re-run `apply_req` if content is ready.\n"
        )
        disc_path.write_text(content, encoding="utf-8")
        return disc_path

    def run_report(self, run_id: str) -> Dict[str, Any]:
        """Return a structured summary of a RUN document."""
        run_path = self.run_dir / f"{run_id}.md"
        if not run_path.exists():
            candidates = list(self.archive_dir.rglob(f"{run_id}.md"))
            if candidates:
                run_path = candidates[0]
            else:
                raise FileNotFoundError(f"RUN not found: {run_id}")
        text = run_path.read_text(encoding="utf-8")
        metadata = self._parse_metadata(text)
        objective = self._extract_section(text, "Objective")
        scope = self._extract_section(text, "Scope")
        output = self._extract_section(text, "Output")
        artifacts = [line[2:].strip() for line in output.splitlines() if line.startswith("- ")]
        return {
            "run_id": run_id,
            "path": str(run_path),
            "status": metadata.get("Status"),
            "objective": objective.strip() if objective else None,
            "scope": scope.strip() if scope else None,
            "validation_state": metadata.get("Verification"),
            "artifacts": artifacts,
        }

    def _extract_section(self, text: str, heading: str) -> str:
        pattern = re.compile(rf"^##\\s+{re.escape(heading)}(?:.*)?$", re.M)
        match = pattern.search(text)
        if not match:
            return ""
        start = match.end()
        next_heading = re.search(r"^##\\s+", text[start:], re.M)
        end = start + next_heading.start() if next_heading else len(text)
        return text[start:end].strip()

    def apply_req(
        self, req_id: str, dry_run: bool = False, create_spec: Optional[object] = "auto"
    ) -> Dict[str, Any]:
        """Orchestrate the pipeline and return a report. Note: Deprecated in v3.4.0."""
        print(f"Warning: apply_req() is deprecated. Use plan_from_brief() for new workflows.")
        report: Dict[str, Any] = {
            "req_id": req_id,
            "dry_run": dry_run,
            "status": "started",
            "artifacts": {},
            "errors": [],
            "disc": None,
        }
        try:
            from core.checks import check_links, check_requirements, lint_metadata

            errors = []
            if not self.validate_req(req_id):
                errors.append(self.last_error or "Validation failed")
            lint_issues = lint_metadata(ROOT_DIR)
            if lint_issues > 0:
                errors.append(f"{lint_issues} lint issue(s) found")
            req_issues = check_requirements(ROOT_DIR)
            if req_issues > 0:
                errors.append(f"{req_issues} requirement issue(s) found")
            link_issues = check_links(ROOT_DIR)
            if link_issues > 0:
                errors.append(f"{link_issues} link issue(s) found")

            if errors:
                raise ValueError("; ".join(errors))

            create_spec_mode = create_spec
            if isinstance(create_spec_mode, str) and create_spec_mode.lower() == "auto":
                create_spec_mode = self._requires_spec(req_id)
            if create_spec_mode not in (True, False):
                create_spec_mode = True

            if dry_run:
                spec_path = (
                    self.spec_dir / f"SPEC-{req_id}.md" if create_spec_mode else None
                )
                run_path = self.run_dir / f"{self._format_run_id(req_id)}.md"
                report["status"] = "planned"
                report["artifacts"] = {
                    "spec_path": str(spec_path) if spec_path else None,
                    "run_path": str(run_path),
                }
                return report
            spec = (
                self.create_spec_draft(req_id, dry_run=False)
                if create_spec_mode
                else None
            )
            run_path = self.create_run(req_id, spec_path=spec, dry_run=False)
            report["status"] = "created"
            report["artifacts"] = {
                "spec_path": str(spec) if spec else None,
                "run_path": str(run_path),
            }
            return report
        except Exception as exc:
            err = str(exc)
            report["status"] = "failed"
            report["errors"].append(err)
            disc = self.create_disc_from_failure(req_id, err)
            report["disc"] = str(disc)
            return report

    def create_disc_from_context(self, context: Dict[str, Any]) -> Path:
        target_id = (
            context.get("req_id")
            or context.get("target_id")
            or context.get("id")
            or "REQ-GEN-000"
        )
        lines = []
        if context.get("stage"):
            lines.append(f"Stage: {context['stage']}")
        if context.get("errors"):
            lines.append("Errors:")
            for item in context["errors"]:
                if isinstance(item, dict):
                    msg = item.get("message") or item.get("type") or str(item)
                else:
                    msg = str(item)
                lines.append(f"- {msg}")
        if context.get("rules"):
            lines.append("Rules:")
            for rule in context["rules"]:
                lines.append(f"- {rule}")
        if context.get("files"):
            lines.append("Files:")
            for file_path in context["files"]:
                lines.append(f"- {file_path}")
        if context.get("logs"):
            lines.append("Logs:")
            lines.append(str(context["logs"]))
        error_log = "\n".join(lines) if lines else "No additional context provided."
        return self.create_disc_from_failure(str(target_id), error_log)

    def _generate_brief_id(self, domain: str = "GEN") -> str:
        """Generate a unique BRIEF ID."""
        # Simple incremental logic: scan existing briefs
        existing = list(self.brief_dir.glob(f"BRIEF-{domain}-*.md"))
        max_idx = 0
        for p in existing:
            match = re.search(r"-(\d{3})\.md$", p.name)
            if match:
                idx = int(match.group(1))
                if idx > max_idx:
                    max_idx = idx
        new_idx = max_idx + 1
        return f"BRIEF-{domain}-{new_idx:03d}"

    def intake(self, description: str, domain: str = "GEN") -> Path:
        """Create a BRIEF from a user request description."""
        self.brief_dir.mkdir(parents=True, exist_ok=True)
        brief_id = self._generate_brief_id(domain)
        date_str = self._now_date()
        
        content = (
            f"# [{brief_id}] Request: {description[:50]}...\n\n"
            f"> **ID**: {brief_id}\n"
            f"> **Date**: {date_str}\n"
            f"> **Status**: Active\n"
            f"> **Template-Version**: {TEMPLATE_VERSION}\n\n"
            "## 1. User Request (원본 요청)\n"
            f"> {description}\n\n"
            "## 2. Intent Summary (의도 요약)\n"
            "> ⚠️ **LLM 작업**: 아래 원본 요청의 핵심 의도를 분석하세요.\n\n"
            "- **주요 목표**: (TBD - LLM이 분석)\n"
            "- **해결할 문제**: (TBD - LLM이 분석)\n"
            "- **CQ 형식 입력 허용**: 정리 안 된 생각/메모도 가능\n\n"
            "## 3. Affected Artifacts (영향받는 문서)\n"
            "> ⚠️ **반드시 구체적인 경로/링크로 작성** (REQ-XXX 금지)  \n"
            "> 예: `02_REQUIREMENTS/capabilities/REQ-AUTH-001.md`\n\n"
            "- **Modify**: (TBD - LLM이 분석)\n"
            "- **Create**: (TBD - LLM이 분석)\n"
            "- **Read**: (TBD - 참고 문서)\n\n"
            "## 4. Proposed Changes (변경 제안)\n"
            "> ⚠️ **LLM 작업**: 구체적인 변경사항을 나열하세요.\n\n"
            "1. (TBD - 구체적 변경사항)\n\n"
            "## 5. Verification Criteria (검증 기준)\n"
            "> ⚠️ **LLM 작업**: 검증 가능한 구체적 조건을 작성하세요.\n\n"
            "- [ ] (TBD - 구체적 검증 조건)\n"
        )
        
        path = self.brief_dir / f"{brief_id}.md"
        path.write_text(content, encoding="utf-8")
        return path

    def _extract_brief_section(self, text: str, heading: str) -> str:
        pattern = re.compile(rf"^##\s*(?:\d+\.)?\s*{re.escape(heading)}(?:.*)?$", re.M)
        match = pattern.search(text)
        if not match:
            return ""
        start = match.end()
        next_heading = re.search(r"^##\s+", text[start:], re.M)
        end = start + next_heading.start() if next_heading else len(text)
        return text[start:end].strip()

    def _resolve_artifact_path(self, path_str: str) -> Path:
        path = Path(path_str)
        if path.is_absolute():
            full = path
        elif path.parts and path.parts[0] == self.root.name:
            full = self.root.parent / path
        else:
            full = self.root / path
        full = full.resolve()
        root = self.root.resolve()
        try:
            full.relative_to(root)
        except ValueError as exc:
            raise ValueError(f"Artifact path must live under {self.root.as_posix()}") from exc
        return full

    def _is_full_path(self, path_str: str) -> bool:
        return ("/" in path_str or "\\" in path_str) and path_str.endswith(".md")

    def _is_req_path(self, path: Path) -> bool:
        req_root = self.req_dir.resolve()
        try:
            path.resolve().relative_to(req_root)
        except ValueError:
            return False
        return True

    def _parse_affected_artifacts(self, text: str) -> List[Dict[str, str]]:
        section = self._extract_brief_section(text, "Affected Artifacts")
        if not section:
            return []
        entries: List[Dict[str, str]] = []
        for line in section.splitlines():
            match = AFFECTED_LINE_RE.match(line)
            if not match:
                continue
            action, target = match.groups()
            target = target.strip()
            link_match = MD_LINK_RE.search(target)
            target_path = link_match.group(1) if link_match else target
            entries.append({"action": action.title(), "raw": target, "path": target_path})
        return entries

    def _create_req_stub(self, req_path: Path, req_id: str) -> None:
        parts = self._req_parts(req_id)
        if not parts:
            raise ValueError(f"Invalid REQ ID format: {req_id}")
        domain = parts["domain"]
        req_path.parent.mkdir(parents=True, exist_ok=True)
        content = (
            f"# [{req_id}] (TBD)\n\n"
            f"> **ID**: {req_id}\n"
            f"> **Domain**: {domain}\n"
            "> **Status**: Draft\n"
            f"> **Last Updated**: {self._now_date()}\n"
            "> **Must-Read**: RULE-ID-001, RULE-META-001\n"
            f"> **Template-Version**: {TEMPLATE_VERSION}\n\n"
            "---\n\n"
            "## Decision\n"
            "- (TBD)\n\n"
            "## Input\n"
            "- (TBD)\n\n"
            "## Output\n"
            "- (TBD)\n\n"
            "## Acceptance Criteria\n"
            "- [ ] (TBD)\n\n"
            "## Validation\n\n"
            "```bash\n"
            "# (TBD)\n"
            "```\n"
        )
        req_path.write_text(content, encoding="utf-8")

    def _touch_req_metadata(self, req_path: Path, status: str = "Active") -> None:
        text = req_path.read_text(encoding="utf-8")
        text = self._update_meta_line(text, "Last Updated", self._now_date())
        if status:
            text = self._update_meta_line(text, "Status", status)
        req_path.write_text(text, encoding="utf-8")

    def plan_from_brief(self, brief_id: str) -> Path:
        """Create a RUN document based on a BRIEF."""
        # Locate brief
        brief_path = self.brief_dir / f"{brief_id}.md"
        if not brief_path.exists():
             raise FileNotFoundError(f"Brief not found: {brief_id}")

        text = brief_path.read_text(encoding="utf-8")

        artifacts = self._parse_affected_artifacts(text)
        errors = []
        if not artifacts:
            errors.append("Affected Artifacts section is missing or empty")

        req_targets: List[Tuple[str, Path]] = []
        for entry in artifacts:
            if not self._is_full_path(entry["path"]):
                errors.append(f"Affected Artifacts must use full paths or links: {entry['raw']}")
                continue
            resolved = self._resolve_artifact_path(entry["path"])
            if self._is_req_path(resolved):
                req_targets.append((entry["action"], resolved))
            elif "REQ-" in entry["path"]:
                errors.append(
                    f"REQ must live under 02_REQUIREMENTS/capabilities: {entry['raw']}"
                )

        if not req_targets:
            errors.append("No REQ entries found in Affected Artifacts.")

        if errors:
            raise ValueError("Brief validation failed: " + "; ".join(errors))

        for action_raw, req_path in req_targets:
            action = action_raw.lower()
            req_id = req_path.stem
            if action == "create":
                if req_path.exists():
                    raise ValueError(f"REQ already exists: {req_path}")
                self._create_req_stub(req_path, req_id)
            elif action == "modify":
                if not req_path.exists():
                    raise FileNotFoundError(f"REQ not found for modify: {req_path}")
                self._touch_req_metadata(req_path, status="Active")

        # Parse Brief ID to create correlated RUN ID? 
        # Or just use the Brief ID as the RUN base?
        # Strategy: RUN-BRIEF-[DOMAIN]-[NNN]-step-01
        
        # Use simple mapping for now
        run_id = f"RUN-{brief_id}-step-01"
        run_path = self.run_dir / f"{run_id}.md"
        
        if run_path.exists():
            # If step-01 exists, maybe increment? sticking to step-01 for simplicity of this logic
            pass
            
        content = (
            f"# [{run_id}] Execution for {brief_id}\n\n"
            f"> **ID**: {run_id}\n"
            f"> **Input**: {brief_id}\n"
            f"> **Status**: Active\n"
            f"> **Started**: {self._now_date()}\n"
            f"> **Verification**: `python memory_manager.py --doctor`\n"
            f"> **Template-Version**: {TEMPLATE_VERSION}\n\n"
            "## Objective (목표)\n"
            f"Execute the requirements defined in {brief_id}. ({brief_id}에 정의된 요구사항 실행)\n\n"
            "## Scope (범위)\n\n"
            "### In Scope\n"
            f"- Implement changes requested in {brief_id}\n"
            "- (추가 범위는 BRIEF의 Affected Artifacts를 참고하여 구체화)\n\n"
            "### Out of Scope\n"
            "- (명시적으로 제외되는 것)\n\n"
            "## Steps (단계)\n"
            "> ⚠️ **LLM 작업**: BRIEF 내용을 반영한 구체적 단계를 작성하세요.\n\n"
            f"- [ ] 1. Review {brief_id} details (브리프 내용 검토)\n"
            "- [ ] 2. Implement code changes (코드 변경 구현)\n"
            f"- [ ] 3. Verify against {brief_id} goals (브리프 목표 검증)\n\n"
            "## Verification (Self-Check)\n"
            "> 작업 완료 전 반드시 확인\n\n"
            "- [ ] **Test**: `pytest` 또는 관련 테스트 통과?\n"
            "- [ ] **Boundary**: CONVENTIONS Boundaries 준수?\n"
            f"- [ ] **Spec**: {brief_id}과 일치?\n"
            "- [ ] **Doctor**: `python memory_manager.py --doctor` 통과?\n\n"
            "## Evidence (Implementation Proof)\n"
            "> 구현 완료 후 작성\n\n"
            "- **Tests**: (통과한 테스트 파일/결과)\n"
            "- **Commands**: (실행한 명령어)\n"
            "- **Code**: (생성/수정된 파일)\n"
            "- **Logs**: (관련 로그)\n\n"
            "## Output (결과물)\n"
            f"- Implemented features from {brief_id} ({brief_id} 기능 구현)\n"
            "- (생성/수정된 구체적 파일 목록)\n"
        )
        
        run_path.write_text(content, encoding="utf-8")
        return run_path
