# API Specifications

> 모듈별 입출력 명세를 이곳에 저장합니다.

## Template
```markdown
# [Module Name] API Specification

> **Module**: (모듈명)
> **Last Updated**: YYYY-MM-DD

---

## Endpoints / Functions

### `GET /api/users/{id}`
- **Description**: 사용자 정보 조회
- **Path Parameters**:
  - `id` (UUID): 사용자 ID
- **Response**:
```json
{
  "id": "uuid",
  "email": "string",
  "created_at": "datetime"
}
```
- **Error Codes**:
  - `404`: User not found
  - `500`: Internal server error

### `function_name(param1, param2) -> ReturnType`
- **Description**: 함수 설명
- **Parameters**:
  - `param1` (Type): 설명
  - `param2` (Type): 설명
- **Returns**: ReturnType 설명
- **Raises**: 예외 상황
```
