# [CQ-DIST-002] pip 패키지 배포

> **ID**: CQ-DIST-002
> **Domain**: DIST
> **Status**: Draft
> **Last Updated**: 2026-02-06

---

## Question
- Atlas CLI를 pip 패키지로 배포하여 `pipx/uv install`로 설치하고 `atlas` 명령어로 실행할 수 있는가?

## Expected Answer (Criteria)
1. `pipx install memory-atlas` (또는 git URL)로 설치 가능
2. 설치 후 `atlas init/doctor/sync` 등 명령어 실행 가능
3. 프로젝트 산출물 구조(.atlas/...)는 기존과 동일하게 유지
4. 프로젝트별 atlas.py 복사 불필요
5. `pipx upgrade`로 버전 업데이트 가능
6. defaults/템플릿은 "프로젝트 로컬 우선" 규칙 적용

## Traceability
- **Supersedes**: CQ-DIST-001 (단일 파일 배포 - 폐기)
- **Solved by**: [REQ-DIST-002](../req/REQ-DIST-002.md)
