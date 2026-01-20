# Task Logs (Execution Layer)

> **Template-Version**: 2.4
>
> 실행 기록을 관리합니다.

## Execution Unit Model (v2.2)

```
실행 문서 1개 = 1목적 + 1검증 + 1결과

RUN-REQ-AUTH-001-step-01.md  (로그인 폼 구현)
RUN-REQ-AUTH-001-step-02.md  (API 연동)
RUN-REQ-AUTH-001-step-03.md  (테스트 작성)
```

### Why Small Units?

- 큰 RUN 금지: 한번 실행에 너무 많은 변경이 묶이면 추적 불가
- 1:1 대응: 변경 이유를 명확히 추적 가능
- 검색 가능: 로그가 쌓여도 의미있는 검색

## Structure

```
04_TASK_LOGS/
├── active/             # 실행 중 (RUN-*)
│   └── RUN-REQ-AUTH-001-step-01.md
└── archive/            # 완료된 작업
    └── YYYY-MM/
        └── RUN-*.md
```

## Naming Convention

`RUN-[REQ|RULE]-[DOMAIN]-[NNN]-step-[NN].md`

Examples:
- `RUN-REQ-AUTH-001-step-01.md`
- `RUN-REQ-AUTH-001-step-02.md`
- `RUN-RULE-DATA-001-step-01.md`
