# Views (VIEW) — 목적 중심 규칙

핵심 목표: 사람이 2~3분 안에 "이 뷰가 다루는 시스템 흐름/논점/경계"를 파악하게 한다. 세부는 SSOT로 위임한다.

1) 메타데이터 강화 (필수)

Last Updated, Status, Refs + 아래 추가

Audience: (예: Dev/Ops/Reviewer)

Intent: 이 문서가 답하려는 1문장 질문 (예: "수집~검색~충돌해소가 품질을 어떻게 보장하는가?")

Scope: In / Out 을 1~3줄로

2) 길이/밀도 제한 (필수)

Hard limit: 본문(References 제외) 최대 120~180 라인 또는 최대 1,200~1,800 단어 중 하나를 선택해 고정.

표/리스트 남발 방지:

표는 최대 3개,

한 섹션의 bullet은 최대 7개,

코드블록은 원칙적으로 금지(필요 시 SSOT로 링크).

이유: 뷰가 SSOT를 복제하는 순간부터 뷰는 유지보수 지옥이 됨.

3) "흐름 지도" 섹션 의무화 (필수)

뷰는 반드시 아래 중 하나를 포함:

## Flow Map (phase/step 다이어그램) 또는

## Key Pipeline (Inputs → Decisions → Outputs) 3단 구조

최소 요건: 입력/결정/출력 각각 3개 이하로 요약.

4) SSOT 위임 규칙 (필수)

뷰 본문에는 세부 정의/알고리즘/스키마의 완전한 기술을 금지하고, 아래 형태로만 허용:

"상세는 SSOT로 위임" 문장 패턴을 강제:

예: "품질 게이트의 축 정의는 SSOT 참조. (@REQ-007#Three-Axis Judgment)"

"뷰에 남겨도 되는 것"만 허용:

단계 간 연결(왜 다음 단계가 필요한지)

의사결정 분기(어떤 조건에서 어느 경로로 가는지)

실패 유형의 지도(어디서 깨지면 어디를 본다)

5) 앵커 규칙 강화 (필수, 현실적인 방식)

현재는 "규범 키워드가 있으면 앵커"인데, 이러면 뷰가 사실을 마음대로 말하기 쉬움. 아래처럼 바꾸는 게 좋아:

**강한 주장(Strong Claim)**은 앵커 필수.

Strong Claim 정의:

수치/임계값/상태 전이/정렬 규칙/우선순위/불변성/보장(재현성 등)

Strong Claim이 아닌 문장은 앵커 선택.

규범 키워드 기반은 유지하되, Strong Claim 트리거를 추가하는 게 핵심.

6) SSOT Index 자동 완결성 규칙 (필수)

## References (SSOT index)에는 본문에서 언급된 SSOT ID를 "전부" 나열(현 규칙 유지).

추가로:

Refs에 있는 SSOT는 반드시 본문에서 최소 1회 이상 실제로 인용되어야 함("Refs만 있고 본문에 안 나오면" 의미가 없음).

7) 변경 안정성 규칙 (권장)

뷰는 "사람 읽기용"이라 자주 바뀌면 혼란.

Status: Draft/Stable/Deprecated로 운영.

Stable 뷰는 SSOT 변경이 있어도 "흐름이 안 바뀌면" 수정하지 않는 원칙.

8) 섹션 템플릿(추천, 단순)

뷰마다 구조가 흔들리면 읽기 경험이 깨져서, 최소 템플릿만 강제:

Summary (3~6줄)

Flow Map (ASCII 가능)

Key Decisions / Failure Modes (각 3~5개)

What to Read Next (SSOT 링크)

References (SSOT index)
