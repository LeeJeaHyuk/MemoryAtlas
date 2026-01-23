# [RULE-FLOW-002] Change Brief Policy

> **ID**: RULE-FLOW-002
> **Domain**: FLOW
> **Priority**: High
> **Last Updated**: 2026-01-23
> **Must-Read**: RULE-ID-001, REQ-MCP-001
> **Template-Version**: 2.4

---

## Rule Statement (최종 결정)

모든 비자명한 변경 요청은 **Change Brief**를 통해 수집되어야 하며, Brief가 승인된 후에만 RUN 문서를 생성할 수 있다.
Intake must be executed via the MCP intake tool, which creates the BRIEF.
If MCP is unavailable, stop and inform the user to fix MCP before proceeding.


---

## Location (Policy File)
This rule must live at `02_REQUIREMENTS/invariants/RULE-FLOW-002.md`.

## Rationale

**Source**: REQ-MCP-001 (3-Phase Workflow)

기존 "즉시 실행" 모델의 문제점:
1. **맥락 소실**: 여러 DISC, 채팅 로그가 흩어져 에이전트가 전체 맥락을 파악하기 어려움
2. **추적 불가**: 요청 → 실행 간 연결고리가 명시적으로 기록되지 않음
3. **검증 누락**: 사전 영향도 분석 없이 바로 실행되어 예상치 못한 부작용 발생

Change Brief는 **단일 스냅샷 문서**로서:
- 흩어진 요구사항을 하나로 압축
- 영향받는 문서(REQ, RULE, ADR)를 사전에 식별
- 검증 기준을 실행 전에 확정

---

## Brief Requirements

### ID 형식

```
BRIEF-[DOMAIN]-[YYYYMMDD]-[SEQ]
```

**Examples:**
- `BRIEF-MCP-20260123-01`
- `BRIEF-VALID-20260124-02`

### 필수 섹션

| Section | Description |
|---------|-------------|
| **Intent Summary** | 사용자가 달성하려는 목표 (1-2 문장) |
| **Affected Artifacts** | Modify/Create/Delete with full paths or markdown links (e.g., 02_REQUIREMENTS/capabilities/REQ-*.md) |
| **Proposed Changes** | 구체적인 변경 내용 (bullet points) |
| **Verification Criteria** | 완료 조건 체크리스트 |

Affected Artifacts must include full paths or markdown links. REQ lives under 02_REQUIREMENTS/capabilities/.

### 저장 위치

```
02_REQUIREMENTS/discussions/briefs/BRIEF-*.md
```

---

## Lifecycle States

```
[Created] → [Under Review] → [Approved] → [Consumed]
```

| State | Description | Allowed Actions |
|-------|-------------|-----------------|
| **Created** | `intake()` 호출로 생성됨 | 수정, 삭제 |
| **Under Review** | 사용자 검토 중 | 수정, 승인, 거절 |
| **Approved** | 사용자가 내용을 확정함 | `plan_from_brief()` 호출 |
| **Consumed** | RUN 문서가 생성됨 | 아카이브 참조만 가능 |

---

## Examples

### ✅ Correct Brief

```markdown
# [BRIEF-MCP-20260123-01] Switch to 3-Phase Workflow

## 1. Intent Summary
MCP 워크플로우를 Intake-Plan-Execute 3단계로 변경하여 맥락 유지를 강화함.

## 2. Affected Artifacts
- Modify: 02_REQUIREMENTS/capabilities/REQ-MCP-001.md
- Create: 02_REQUIREMENTS/invariants/RULE-FLOW-002.md

## 3. Proposed Changes
- `kick_off` 도구 삭제 및 `intake` 도구 신설
- `briefs` 폴더 구조 생성

## 4. Verification Criteria
- [ ] `intake` 호출 시 BRIEF 파일 생성 확인
- [ ] `plan_from_brief` 호출 시 RUN 파일 생성 확인
```

### ❌ Incorrect Brief

```markdown
# MCP 변경
워크플로우를 바꾸겠습니다.
```

**오류**: ID 형식 누락, 필수 섹션 미포함

---

## RUN Document Linking

RUN 문서는 반드시 원본 Brief를 참조해야 한다:

```markdown
# [RUN-REQ-MCP-001-step-01] Implement 3-Phase Workflow

> **ID**: RUN-REQ-MCP-001-step-01
> ...
> **Must-Read**: BRIEF-MCP-20260123-01, REQ-MCP-001
```
Note: Use the run_id returned by plan_from_brief; do not assemble RUN IDs by hand.

이를 통해 에이전트는 Brief와 RUN만 보고 전체 맥락을 파악할 수 있다.

---

## Validation

```bash
# Brief 파일 형식 검증 (--lint 확장)
python memory_manager.py --lint

# Brief → RUN 연결 검증
python memory_manager.py --links
```

---

## Exceptions

### Brief 없이 RUN 생성 가능한 경우

1. **긴급 핫픽스**: 프로덕션 장애 대응 시 (사후 Brief 작성 필수)
2. **문서 오타 수정**: 내용 변경 없는 단순 수정
3. **자동화된 유지보수**: `--doctor` 자동 수정 등

위 예외 시에도 RUN 문서의 `Notes` 섹션에 예외 사유를 명시해야 한다.




