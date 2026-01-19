# Requirements (WHAT)

> 이 폴더는 **"무엇을 만들 것인가?"**를 정의합니다.
> 기능(Feature)과 비즈니스 규칙(Business Rule)을 분리하여 관리합니다.

## Structure

```
02_REQUIREMENTS/
├── features/           # 개별 기능 명세
│   └── REQ-XXX-*.md    # 기능별 문서
└── business_rules/     # 비즈니스 로직/공식
    └── RULE-XXX-*.md   # 규칙별 문서
```

## Why Separate?
- **Features**: "뉴스를 크롤링한다", "DB에 저장한다" 같은 동작
- **Business Rules**: "응답 속도는 1초 이내", "모든 시간은 UTC" 같은 제약

AI가 기능 구현에 집중하다가 규칙을 놓치지 않도록 분리합니다.

## Naming Convention
- Features: `REQ-[DOMAIN]-[NUMBER].md` (예: `REQ-AUTH-001.md`)
- Rules: `RULE-[DOMAIN]-[NUMBER].md` (예: `RULE-DATA-001.md`)
