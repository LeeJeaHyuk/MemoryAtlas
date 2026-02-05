# [REQ-DIST-001] 단일 파일 배포 시스템

> **ID**: REQ-DIST-001
> **Domain**: DIST
> **Status**: Implemented
> **Last Updated**: 2026-01-26
> **Answers**: [CQ-DIST-001](../cq/CQ-DIST-001.md)
> **Must-Read**: None

---

## Decision

### 1. 빌드 프로세스 (`build.py`)

```
src/atlas_cli.py (원본 소스)
    ↓ Base64 인코딩
    ↓ EMBEDDED_SRC_B64 변수에 삽입
src/.system_defaults (기본 문서)
    ↓ Base64 인코딩 (JSON)
    ↓ EMBEDDED_DEFAULTS_B64 변수에 삽입
    ↓ stickytape 번들링
atlas.py (단일 배포 파일)
```

### 2. 임베드 메커니즘

| 단계 | 설명 |
|------|------|
| 인코딩 | 원본 소스를 Base64로 인코딩 |
| 삽입 | `EMBEDDED_SRC_B64` 상수에 저장 |
| 디코딩 | `init` 시 Base64 디코딩하여 파일 생성 |
| 기본 문서 | `src/.system_defaults` 내용을 Base64(JSON)로 인코딩하여 `EMBEDDED_DEFAULTS_B64`로 임베드 |
| 폴백 | 배포 환경에서 `src/.system_defaults`가 없을 때 임베드된 기본 문서를 사용 |

### 3. init 시 생성되는 구조

```
.atlas/
├── .system/
│   ├── src/
│   │   └── atlas_cli.py    ← 원본 소스 (디코딩됨)
│   ├── templates/
│   ├── prompts/
│   ├── state/
│   ├── VERSION
│   └── VERSIONING.md
├── req/
├── rule/
├── cq/
├── brief/
├── runs/
└── idea/
```

---

## Input
- `src/atlas_cli.py` (원본 소스 코드)

## Output
- `atlas.py` (번들링된 단일 배포 파일)
- `.atlas/.system/src/atlas_cli.py` (init 시 생성되는 원본 소스)

---

## Acceptance Criteria
- [x] `build.py` 실행 시 원본 소스가 Base64로 인코딩됨
- [x] `atlas.py`에 `EMBEDDED_SRC_B64` 상수로 소스가 포함됨
- [x] `atlas.py`에 `EMBEDDED_DEFAULTS_B64` 상수로 기본 문서가 포함됨
- [x] `atlas.py init` 실행 시 `.atlas/.system/src/atlas_cli.py` 생성
- [x] 생성된 소스가 원본과 동일 (stickytape wrapper 없음)
- [x] 외부 파일 의존성 없이 `atlas.py` 단독 동작

---

## Implementation

### build.py 주요 로직
```python
# 원본 소스 Base64 인코딩
original_src = src.read_text(encoding="utf-8")
embedded_b64 = base64.b64encode(original_src.encode("utf-8")).decode("ascii")

# 기본 문서 Base64(JSON) 인코딩
defaults_json = json.dumps(embedded_defaults, ensure_ascii=False, sort_keys=True)
defaults_b64 = base64.b64encode(defaults_json.encode("utf-8")).decode("ascii")

# stickytape 번들링 후 placeholder 교체
output = output.replace(
    'EMBEDDED_SRC_B64 = "__EMBEDDED_SRC_PLACEHOLDER__"',
    f'EMBEDDED_SRC_B64 = "{embedded_b64}"'
)
output = output.replace(
    'EMBEDDED_DEFAULTS_B64 = "__EMBEDDED_DEFAULTS_PLACEHOLDER__"',
    f'EMBEDDED_DEFAULTS_B64 = "{defaults_b64}"'
)
```

### atlas_cli.py 로드 로직
```python
def load_default_src_files() -> dict[str, str]:
    # 개발 모드: src/.system_defaults/src/에서 로드
    # 배포 모드: EMBEDDED_SRC_B64에서 디코딩
    if EMBEDDED_SRC_B64 != "__EMBEDDED_SRC_PLACEHOLDER__":
        decoded = base64.b64decode(EMBEDDED_SRC_B64).decode("utf-8")
        files["atlas_cli.py"] = decoded
    return files
```

```python
def load_default_templates() -> dict[str, str]:
    # 개발 모드: src/.system_defaults/templates에서 로드
    # 배포 모드: EMBEDDED_DEFAULTS_B64에서 디코딩
    if EMBEDDED_DEFAULTS_B64 != "__EMBEDDED_DEFAULTS_PLACEHOLDER__":
        defaults = json.loads(base64.b64decode(EMBEDDED_DEFAULTS_B64))
        templates[name] = defaults[f"templates/{name}"]
    return templates
```

---

## Traceability
- **Answers**: [CQ-DIST-001](../cq/CQ-DIST-001.md)
