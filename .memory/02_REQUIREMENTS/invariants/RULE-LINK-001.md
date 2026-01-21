# [RULE-LINK-001] Document Link Validation Rules

> **ID**: RULE-LINK-001
> **Domain**: VALIDATION
> **Priority**: High
> **Last Updated**: 2026-01-20
> **Must-Read**: RULE-DIR-001
> **Template-Version**: 2.4

---

## Rule Statement (최종 결정)

모든 MemoryAtlas 문서 내 마크다운 링크는 유효한 경로를 가리켜야 하며, 상대 경로 사용을 원칙으로 한다.

---

## Rationale

**Source**: `src/core/checks.py:iter_links(), check_links()`
**Regex**: `src/core/config.py:95` - `LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")`

링크가 깨지면:
1. AI가 Must-Read 문서를 찾지 못함
2. 문서 간 종속성 추적 불가
3. 사용자가 관련 문서 탐색 실패

자동 링크 검증(`--links`)을 통해 문서 무결성을 보장한다.

---

## Link Format Rules

### ✅ Allowed Link Types

1. **상대 경로** (권장)
   ```markdown
   [RULE-DATA-001](../business_rules/RULE-DATA-001.md)
   [Architecture](../../03_TECH_SPECS/architecture/SYSTEM.md)
   ```

2. **앵커 링크** (같은 문서 내)
   ```markdown
   [Jump to Examples](#examples)
   ```

3. **외부 URL**
   ```markdown
   [Python Docs](https://docs.python.org/)
   ```

### ⚠️ Conditional: 절대 경로
```markdown
[File](/absolute/path/to/file.md)
```

**기본적으로 금지**되지만 `--allow-absolute-links` 플래그로 허용 가능.

---

## Examples

### ✅ Correct

```markdown
- Must-Read: [RULE-ID-001](RULE-ID-001.md)
- Related: [ADR-003](../../03_TECH_SPECS/decisions/ADR-003.md)
- See [Implementation Details](#implementation)
```

### ❌ Incorrect

```markdown
# 존재하지 않는 파일
- Must-Read: [RULE-FAKE-999](

../business_rules/RULE-FAKE-999.md)

# 깨진 상대 경로
- Related: [ADR-003](wrong/path/ADR-003.md)

# 잘못된 앵커
- See [Details](#non-existent-section)
```

---

## Validation

```bash
# 링크 검증
python memory_manager.py --links

# 절대 경로 링크 허용하며 검증
python memory_manager.py --links --allow-absolute-links
```

**출력 예시**:
```
! Broken link in 02_REQUIREMENTS/features/REQ-AUTH-001.md: ../business_rules/RULE-FAKE-999.md
Link check: 1 issue(s)
```

---

## Exceptions

### 자동 제외 항목

1. **코드 블록 내 링크** (```...``` 안)
2. **외부 URL** (`http://`, `https://`)
3. **앵커만 있는 링크** (`#section`)
4. **README.md, 00_INDEX.md** 등 스킵 파일

---

## Special Cases

### Must-Read 링크

Must-Read 필드에 링크를 사용할 때는 **링크 텍스트가 반드시 ID여야 함**:

```markdown
> **Must-Read**: [RULE-SEC-001](../business_rules/RULE-SEC-001.md), ADR-003
```

위 예시에서:
- ✅ `[RULE-SEC-001]` - 링크 텍스트가 ID
- ✅ `ADR-003` - ID만 명시 (링크 없음)
- ❌ `[보안 규칙](RULE-ID-001.md)` - 링크 텍스트가 ID 아님
