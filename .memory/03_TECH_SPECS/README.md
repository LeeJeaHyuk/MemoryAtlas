# Technical Specifications (HOW)

> **Template-Version**: 3.0
>
> **"어떻게 만들 것인가?"**를 정의합니다.

## Structure

```
03_TECH_SPECS/
├── architecture/       # 구조도, DB 스키마
├── api_specs/          # 입출력 명세
└── decisions/          # ADR (RATIONALE)
```

## Relation to Authority

```
REQ (Authority) → TECH_SPEC (Implementation) → CODE
```

TECH_SPEC은 REQ의 결정을 **구현**하는 방법을 정의합니다.
REQ와 충돌 시, REQ가 우선합니다.
