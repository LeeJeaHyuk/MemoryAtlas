# Task Logs (HISTORY)

> 작업 기록을 관리합니다.
> 진행 중(active)과 완료(archive)를 분리합니다.

## Structure

```
04_TASK_LOGS/
├── active/             # 현재 작업 중
│   └── YYYY-MM-DD_TYPE_Description.md
└── archive/            # 완료된 작업
    └── YYYY-MM/        # 월별 정리
        └── *.md
```

## Workflow
1. **Create**: 새 작업은 `active/`에 생성
2. **Execute**: 작업 중 상태 업데이트
3. **Archive**: 완료 시 `archive/YYYY-MM/`로 이동

## Naming Convention (MANDATORY)
`[YYYY-MM-DD]_[Type]_[ShortDescription].md`

### Types
| Type | Description |
|------|-------------|
| `FEAT` | 새 기능 |
| `FIX` | 버그 수정 |
| `DOCS` | 문서화 |
| `REFACTOR` | 코드 정리 |
| `MAINT` | 유지보수 |

### Examples
- `2024-01-16_FEAT_UserLogin.md`
- `2024-01-17_FIX_MemoryLeak.md`
