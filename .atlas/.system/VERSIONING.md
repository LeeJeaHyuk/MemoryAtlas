# Atlas Versioning Policy

> **Current Version**: See [VERSION](./VERSION)

---

## Version Format

```
MAJOR.MINOR.PATCH
```

Atlas는 **스키마 버전**(Workspace 구조/문서 템플릿/메타데이터 규칙)을 기준으로 버전을 관리합니다.
CLI는 이 VERSION 파일을 읽어 표시만 합니다 (SSOT 원칙).

---

## Version Bump Rules

### PATCH (+0.0.1)

**호환성 유지, 동작 변경 없음**

- 문서 오타/주석/출력 문구 수정
- 검증 결과나 파싱에 영향 없는 변경
- 내부 리팩토링 (외부 계약 동일)

예시:
- `doctor` 출력 메시지 개선
- 템플릿 주석 보완

### MINOR (+0.1.0)

**하위 호환, 기능 추가**

- 새로운 문서 타입/필드 **추가** (기존은 그대로 유효)
- 새 CLI 명령 추가, 기존 동작 유지
- validator 규칙 추가 (단, default는 warning이거나 기존 통과 보장)

예시:
- `atlas archive` 명령 추가
- SPEC.md 템플릿 타입 추가
- 새 메타데이터 필드 (optional)

### MAJOR (+1.0.0)

**호환성 깨짐, 마이그레이션 필요**

- 폴더 구조 변경
- 필드 이름 변경/필수화
- 기존 문서가 마이그레이션 없이는 fail 나는 변경
- CLI 명령 인터페이스 변경 (기존 스크립트 깨짐)

예시:
- `.atlas/runs` → `.atlas/log` 폴더명 변경
- `Brief` 메타 필드 → `Source` 로 변경
- `--git` 옵션 필수화

---

## Compatibility Contract

> **핵심 원칙**: 같은 MINOR 버전 내에서는 기존 문서가 그대로 동작해야 한다.

| 버전 범위 | 호환성 보장 |
|-----------|-------------|
| `0.1.x` | 동일 스키마 계약. 0.1.0 문서는 0.1.9에서도 통과 |
| `0.2.0` | 0.1.x 문서를 그대로 읽고 통과해야 함 |
| `1.0.0` | 0.x → 1.0 마이그레이션 가이드 제공 필수 |

### 0.x 특수 규칙

개발 단계(`0.x.x`)에서도 위 규칙을 준수합니다.
"0.x니까 막 바꿔도 된다"는 관행을 따르지 않습니다.

---

## Operational Rules

### 버전 업데이트 시점

1. **VERSION 파일 변경**은 기능 커밋에 포함하거나 단독 커밋
2. **커밋 메시지**: `chore(schema): bump to 0.2.0`
3. **Git 태그**: `git tag v0.2.0`

### CHANGELOG (권장)

```markdown
## [0.2.0] - YYYY-MM-DD

### Added
- `atlas archive` 명령 추가

### Changed
- doctor 출력 포맷 개선

### Fixed
- BRIEF 상태 동기화 버그 수정
```

---

## Version Check

```bash
python atlas.py --version
# Atlas 0.1.0
```
