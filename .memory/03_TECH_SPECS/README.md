# Technical Specifications (HOW)

> 이 폴더는 **"어떻게 만들 것인가?"**를 정의합니다.
> 구조(Architecture), 인터페이스(API), 의사결정(Decisions)을 분리합니다.

## Structure

```
03_TECH_SPECS/
├── architecture/       # 구조도, DB 스키마 (비교적 덜 변함)
├── api_specs/          # 입출력 명세 (자주 변함)
└── decisions/          # 기술적 의사결정 기록 (ADR)
```

## Why This Structure?
- **Architecture**: 전체 그림. 자주 바뀌지 않음.
- **API Specs**: 구현 세부사항. 자주 바뀜.
- **Decisions**: "왜 이렇게 했는가?" 기록. 나중에 후회하지 않기 위해.
