# Requirements (Authority Layer)

> **Template-Version**: 3.3
>
> 이 폴더는 **"무엇을 만들 것인가?"**의 **최종 결정**을 저장합니다.
> 논의/조율 기록은 `discussions/`에 분리합니다.

## Capabilities & Invariants Model (v3.0)

```
문서 등급:
├── capabilities/    → REQ-* (기능/행동) "시스템은 ~해야 한다"
├── invariants/      → RULE-* (불변 규칙) "항상 ~이다 / ~는 금지"
└── discussions/     → DISC-* (조율 기록, LLM 기본 무시)
```

## REQ vs RULE 판정 기준

### REQ (capabilities/에만 존재)
- **문장 형태**: "시스템은 ~~해야 한다" (동작 중심)
- **필수 섹션**: Input, Output, Acceptance Criteria
- **규칙 작성 금지**: 형식/제약/금지는 Must-Read로 RULE 참조

### RULE (invariants/에만 존재)
- **문장 형태**: "항상 ~~이다 / ~~는 금지" (불변 중심)
- **필수 섹션**: Scope, Violation 판정 기준, Examples
- **테스트 가능**: 단독으로 참/거짓 판정 가능해야 함

## Structure

```
02_REQUIREMENTS/
├── capabilities/       # REQ-* (기능/행동)
│   └── REQ-AUTH-001.md
├── invariants/         # RULE-* (불변 규칙)
│   └── RULE-ID-001.md
└── discussions/        # DISC-* (조율 기록)
    └── DISC-AUTH-001.md
```

## Naming Convention (STRICT)

| Type | Pattern | Example | Location |
|------|---------|---------|----------|
| Capability | `REQ-[DOMAIN]-[NNN].md` | `REQ-AUTH-001.md` | capabilities/ |
| Invariant | `RULE-[DOMAIN]-[NNN].md` | `RULE-ID-001.md` | invariants/ |
| Discussion | `DISC-[DOMAIN]-[NNN].md` | `DISC-AUTH-001.md` | discussions/ |

## Must-Read Field (Required)

모든 REQ/RULE 문서에는 `**Must-Read**` 필드가 필수입니다:

```markdown
> **Must-Read**: RULE-ID-001, RULE-META-001, ADR-003
```

이 필드에 나열된 문서는 해당 REQ 구현 시 **반드시** 읽어야 합니다.

- Must-Read allows only RULE/ADR IDs (CTX is P0 and not allowed here).
- If you use markdown links, the link text must be the ID (e.g. `[RULE-ID-001](invariants/RULE-ID-001.md)`).

## Partial Updates Policy (Recommended)

- Keep REQ as the full contract; `Status=Active` means the whole REQ is executable.
- Do not mix "pending/later" items inside an Active REQ. Use DISC or a new Draft REQ.
- When only part changes, narrow scope in RUN (In Scope / Out of Scope) and reference the target sections.
- Record evidence in RUN for "already implemented" vs "needs work":
  tests passed, commands run, and code locations.

### When to Revisit a Pending Section Model

Adopt a formal Pending section only if at least two are true:
- A single REQ routinely contains 10+ sub-features and only a subset is delivered each time.
- Agents frequently misjudge scope, causing repeated rework.
- There are multiple collaborators and explicit sprint deferrals are required.
- Roadmap-level proposals must live inside the REQ.

## MCP Automation Notes

- `Automator.apply_req(req_id[, dry_run, create_spec])` drives the pipeline: validate REQ, build a spec draft (optional), create a RUN, and generate DISC drafts on failure.
- The CLI exposes `python memory_manager.py apply-req --id REQ-XXX-001 [--dry-run] [--no-spec]`; it prints artifacts or failure/discussion links.
- FastMCP agents can call `src/mcp_server.py::apply_req` to run the same flow and receive a JSON-like report.
- Read-only MCP helpers: `req_status(req_id)` for readiness checks, `run_report(run_id)` for structured RUN summaries.


