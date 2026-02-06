# [REQ-DIST-002] pip 패키지 배포 시스템

> **ID**: REQ-DIST-002
> **Domain**: DIST
> **Status**: Draft
> **Last Updated**: 2026-02-06
> **Answers**: [CQ-DIST-002](../cq/CQ-DIST-002.md)
> **Must-Read**: None
> **Supersedes**: REQ-DIST-001

---

## Decision

### 1. 패키지 구조

```
memory-atlas/
├── pyproject.toml
├── README.md
└── src/
    └── memory_atlas/
        ├── __init__.py
        ├── cli.py              # CLI entrypoint
        ├── defaults.json       # 기본 템플릿/문서
        └── core/
            ├── init.py
            ├── doctor.py
            ├── sync.py
            └── ...
```

### 2. 설치 방식

| 방식 | 명령어 |
|------|--------|
| pipx (권장) | `pipx install memory-atlas` |
| uv | `uv tool install memory-atlas` |
| pip (개발) | `pip install -e .` |
| git URL | `pipx install git+<repo_url>` |

### 3. CLI entrypoint

```toml
# pyproject.toml
[project.scripts]
atlas = "memory_atlas.cli:main"
```

### 4. defaults 로딩 우선순위

1. `<project_root>/.atlas/.system/defaults.json` (프로젝트 로컬)
2. 환경변수 `ATLAS_DEFAULTS=/path/to/defaults.json`
3. 패키지 내장 `memory_atlas/defaults.json` (fallback)

### 5. 프로젝트 산출물 구조 (불변)

```
.atlas/
├── .system/
│   ├── templates/
│   ├── prompts/
│   ├── state/
│   └── VERSION
├── req/
├── rule/
├── adr/
├── cq/
├── views/
├── runs/
├── drafts/
└── inbox/
```

---

## Input
- `src/memory_atlas/` (패키지 소스)
- `pyproject.toml` (빌드 설정)

## Output
- PyPI 패키지 또는 git 설치 가능한 패키지
- `atlas` CLI 명령어

---

## Acceptance Criteria
- [ ] `pipx install` 후 `atlas --help` 정상 동작
- [ ] `atlas init` 결과가 기존 atlas.py init과 동일
- [ ] `atlas doctor` 동일한 검증 수행
- [ ] `atlas sync` 동일하게 동작
- [ ] 프로젝트에 atlas.py 복사 불필요
- [ ] `pipx upgrade`로 업데이트 가능
- [ ] 프로젝트 로컬 defaults가 패키지 기본값보다 우선

---

## Migration (기존 프로젝트)

### 권장: 완전 제거
1. 프로젝트에서 `atlas.py` 삭제
2. `pipx install memory-atlas`
3. `atlas doctor`로 정합성 확인

### 선택: Thin Wrapper (점진적 전환)
```python
# atlas.py (10줄 래퍼, 임시)
from memory_atlas.cli import main
if __name__ == "__main__":
    raise SystemExit(main())
```

---

## Traceability
- **Answers**: [CQ-DIST-002](../cq/CQ-DIST-002.md)
- **Supersedes**: REQ-DIST-001 (단일 파일 배포 - 폐기)
