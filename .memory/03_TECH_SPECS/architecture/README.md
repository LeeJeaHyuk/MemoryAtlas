# Architecture Documents

> 시스템 구조도, DB 스키마(ERD), 데이터 흐름도를 이곳에 저장합니다.

## Template: System Architecture
```markdown
# System Architecture

> **Last Updated**: YYYY-MM-DD

---

## High-Level Diagram
(ASCII 다이어그램 또는 이미지 링크)

## Components
| Component | Responsibility | Technology |
|-----------|---------------|------------|
| Frontend | UI | React |
| Backend | API | FastAPI |
| Database | Storage | PostgreSQL |

## Data Flow
1. User → Frontend
2. Frontend → Backend API
3. Backend → Database
```

## Template: Database Schema
```markdown
# Database Schema

> **Last Updated**: YYYY-MM-DD

---

## ERD
(ERD 다이어그램)

## Tables

### users
| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID | PK |
| email | VARCHAR(255) | UNIQUE, NOT NULL |
| created_at | TIMESTAMP | NOT NULL |

### 다른 테이블...
```
