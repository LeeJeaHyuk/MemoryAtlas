# MemoryAtlas

MemoryAtlas는 `.memory` 폴더에 프로젝트 문맥을 구조화하고 문서 규칙을 검증하는 메모리 기반 개발 도구입니다.

## 주요 기능
- `.memory` 구조 초기화/업데이트
- 구조/메타데이터/링크/REQ/RUN 검증 (`--doctor` 또는 개별 체크)
- LLM 프로젝트 킥오프용 부트스트랩 프롬프트 생성 (`--bootstrap`)
- 작업 상태 요약 리포트 출력 (`--status`)

## 요구 사항
- Python 3.x (표준 라이브러리만 사용)

## 빠른 시작
```bash
python memory_manager.py
python memory_manager.py --doctor
python memory_manager.py --status
python memory_manager.py --bootstrap
```

## 자주 쓰는 명령
```bash
python memory_manager.py --check     # 구조 검사
python memory_manager.py --lint      # 문서 메타데이터 검사
python memory_manager.py --links     # 링크 검사
python memory_manager.py --req       # REQ/RULE 검증
python memory_manager.py --runs      # RUN 문서 검증
python memory_manager.py --dry-run   # 변경 사항 미리보기
```

## 디렉터리 구조 (요약)
```
.memory/
  00_SYSTEM/            # 시스템 관리 영역 (자동 관리)
  01_PROJECT_CONTEXT/   # 목표, 규칙, 가이드
  02_REQUIREMENTS/      # REQ/RULE (권한 문서)
  03_TECH_SPECS/        # 기술 사양, ADR
  04_TASK_LOGS/         # RUN 로그 (작업 이력)
  98_KNOWLEDGE/         # 지식/트러블슈팅 아카이브
```

## 참고 사항
- `00_SYSTEM`은 `memory_manager.py`가 관리하므로 직접 수정하지 않는 것을 권장합니다.
- 커스텀 규칙은 `01_PROJECT_CONTEXT/01_CONVENTIONS.md`에 작성하세요.
