# Finance Dashboard Backend

A role-based financial records management system built with Flask and MySQL.

---

## Tech Stack

| Layer          | Choice                  |
|----------------|-------------------------|
| Framework      | Flask                   |
| Database       | MySQL + Flask-SQLAlchemy|
| Auth           | Flask-JWT-Extended      |
| Validation     | Custom + Marshmallow    |
| Migrations     | Flask-Migrate (Alembic) |
| Password Hash  | Flask-Bcrypt            |

---

## Why Flask
Its a lightweight framework and does not impose a project structure or bundle feature that this project does not need. Every component, the ORM,
the auth layer, the validation, is wired in consciously. This makes the architecture easier to read and reason about, which matters for a backend that is being evaluated for clarity of thinking.

Its allows for rapid development without compromising in security, features and structure. Some of its features are - 
- **Lightweight and explicit.**
- **Blueprints map cleanly to domains.** 


## Why MySQL

Financial data is relational by nature. Users own records. Records belong to
categories. Roles govern users. These relationships are explicit and fixed,
which is exactly what a relational database is designed for.


**JOINs are natural here.** Dashboard aggregations like category-wise totals
and monthly trends require grouping across related tables. SQL aggregation
with GROUP BY and SUM is the right tool for this, not application-level
computation.

**Schema enforcement.** MySQL enforces column types, foreign key constraints,
and NOT NULL rules at the database level, not just the application level. This
is a second line of defense after application validation.

**SQLAlchemy as the ORM.** Flask-SQLAlchemy gives clean Python model
definitions while still allowing raw SQL when needed. Flask-Migrate (Alembic)
handles schema changes through versioned migration files, which is the
production-standard approach.

The alternative that i considered was MongoDB. Document databases are flexible and uses BJSON format but
that flexibility works against financial data where the schema should be
strict and relationships should be enforced. MongoDB was ruled out because
the lack of joins would push relationship handling into the application layer,
adding complexity without benefit. Although the joins could be achieved by the aggregation pipeline, but i feel that for this project, MySQL was the best option.

---

## Database Schema

The schema has five tables. Every design decision is intentional.

<img width="1824" height="1278" alt="image" src="https://github.com/user-attachments/assets/43deed47-2d8f-4161-85cb-ac1630d8cb56" />


### `roles`
```sql
id          UUID PRIMARY KEY
name        VARCHAR(50) UNIQUE NOT NULL   -- viewer | analyst | admin
description VARCHAR(255)
```

Roles are stored as a table rather than an enum on the users table. This
means new roles can be added without a schema migration. The application's
role-based access control reads role names at runtime, so adding a new role
is a single INSERT, not a code change.
There are currently 3 roles - viewer, analyst and admin

### `users`
```sql
id            UUID PRIMARY KEY
role_id       INT FK -> roles.id
name          VARCHAR(100) NOT NULL
email         VARCHAR(150) UNIQUE NOT NULL
password_hash VARCHAR(255) NOT NULL
status        VARCHAR(20) DEFAULT 'active'
created_at    DATETIME
updated_at    DATETIME
```

`status` stores whether the account is enabled, not whether the user is
online. Active/inactive is an admin-controlled state. Inactive users are
rejected at the auth middleware layer before any route logic runs.

`password_hash` stores a bcrypt hash. Passwords are never stored or logged
in plain text anywhere in the system.

`updated_at` uses SQLAlchemy's `onupdate` trigger so it is maintained
automatically without application code.

### `categories`
```sql
id   UUID PRIMARY KEY
name VARCHAR(100) UNIQUE NOT NULL
type ENUM(20) NOT NULL   -- income | expense
```

Categories are a lookup table rather than a text field on financial
records. This prevents data inconsistency (salary vs Salary vs SALARY) and
makes category-wise aggregation queries reliable for dashboard. The `type` field on a
category defines whether it is an income or expense category which is an enum and speeds
up dashboard queries that need to separate the two.

### `financial_records`
```sql
id          UUID PRIMARY KEY
user_id     UUID FK -> users.id
category_id UUID FK -> categories.id
amount      DECIMAL(12, 2) NOT NULL
type        ENUM(20) NOT NULL   -- income | expense
notes       TEXT
record_date DATE NOT NULL
is_deleted  BOOLEAN DEFAULT FALSE
created_at  DATETIME
updated_at  DATETIME
```

`type` is stored directly on the record even though it can be derived from
the category. Dashboard queries that filter or group by income vs expense do not need a JOIN to the categories
table to get this field. It trades a small amount of storage for significantly
simpler and faster aggregation queries.

`record_date` is a DATE field separate from `created_at`. A user entering a
past transaction should record when it happened, not when they entered it into
the system. `created_at` tracks system insertion time, `record_date` tracks
the actual financial event.

`is_deleted` implements soft delete. Financial records should not be
permanently destroyed. Soft delete preserves the audit trail, allows admins
to recover mistaken deletions, and keeps historical aggregations accurate.

### `audit_logs`
```sql
id         UUID PRIMARY KEY
user_id    UUID FK -> users.id
action     VARCHAR(50) NOT NULL   -- CREATE | UPDATE | DELETE
table_name VARCHAR(50) NOT NULL
record_id  INT
created_at DATETIME
```


---

## Project Structure

```
.
├── server.py                         # entry point
│
├── Dockerfile                        # containerization for deployment
│
├── logs/
│   └── app.log                       # file-based logs written by logger.py
│
└── app/                              # core application package
    ├── __init__.py                   # app factory 
    ├── config.py                     # DevelopmentConfig, ProductionConfig, TestingConfig classes
    ├── extensions.py                 # db, jwt, bcrypt, migrate instances (initialized without app)
    │
    ├── models/                       # SQLAlchemy ORM models, one file per table
    │   ├── __init__.py               
    │   ├── role.py                 
    │   ├── user.py                   
    │   ├── category.py               
    │   ├── financial_record.py      
    │   └── audit_log.py              
    │
    ├── routes/                       # Flask blueprints, HTTP layer only (no business logic)
    │   ├── __init__.py               
    │   ├── auth_routes.py            
    │   ├── user_routes.py            
    │   ├── role_routes.py           
    │   ├── record_routes.py          
    │   ├── category_routes.py        
    │   ├── dashboard_routes.py       
    │   └── health_routes.py          
    │
    ├── services/                     # business logic layer, called by routes, calls models
    │   ├── auth_service.py          
    │   ├── user_service.py          
    │   ├── role_service.py          
    │   ├── record_service.py        
    │   ├── category_service.py      
    │   └── dashboard_service.py    
    │
    ├── middleware/                   # decorators that run before route handlers
    │   ├── auth.py                   #  verifies JWT and loads g.current_user
    │   └── role.py                   # checks currentuser role
    │
    └── utils/                        
        ├── enums.py                  # constants like RoleType, RecordType, UserStatus
        ├── validator.py              # input validation functions, raises ValueError on bad input
        ├── response.py               # success_response() and error_response() for consistent JSON shape
        ├── pagination.py             # extracts page/limit from query params, paginates SQLAlchemy query
        ├── audit.py                  # log_action() writes to audit_logs, get_recent_activity()
        ├── date_helpers.py           # date range builders for monthly/weekly trend queries
        └── logger.py                 # configures Python logging, writes to logs/app.log
```

## Access Control

Three roles with distinct permissions:

| Action                  | Viewer | Analyst | Admin |
|-------------------------|--------|---------|-------|
| View own records        | yes    | yes     | yes   |
| View all records        | no     | no      | yes   |
| Create records          | no     | yes     | yes   |
| Update own records      | no     | yes     | yes   |
| Delete own records      | no     | yes     | yes   |
| Update any record       | no     | no      | yes   |
| Delete any record       | no     | no      | yes   |
| View dashboard summary  | yes    | yes     | yes   |
| View category totals    | no     | yes     | yes   |
| View monthly trends     | no     | yes     | yes   |
| Manage users            | no     | no      | yes   |
| View recent activity    | no     | no      | yes   |

Access control is enforced in two layers. The `@login_required` decorator
verifies the JWT token and checks the user is active. The `@require_role`
decorator checks the user's role against the allowed roles for that route.
Both run before any route logic executes.

---

## Authentication

JWT (JSON Web Tokens) via Flask-JWT-Extended.

- Login returns an access token (currently for testing its 3 days) and a refresh token (7 days)
- Every protected route requires `Authorization: Bearer <access_token>`
- Inactive users are rejected at the middleware layer regardless of token validity

JWT was chosen over Flask session + Redis (It will be implemented in production) because this is a REST API backend.
Sessions require cookie handling and server-side state, which adds
infrastructure complexity (Redis) and CORS complications when the frontend
and backend are on different origins.
---

## Error Handling

Errors are raised as `ValueError` in validators and services with descriptive
messages. Routes catch them and return consistent JSON error responses.

Every response follows the same envelope:
```json
{
  "status": "success" | "error",
  "message": "human readable message",
  "data": null | { ... }
}
```

HTTP status codes are used correctly. 400 for bad input, 401 for missing or
invalid auth, 403 for insufficient permissions, 404 for missing resources.

---

## Additional Thoughtfulness

1) **Validation** Implemented a custom layer of validation for values, types, formats etc in ```app/utils/validation.py```
2) **Pagination** All GET routes are completely paginated.
3) **Custom Request Response**
4) **JWT Authentication**
5) **logger** Implemented a custom logger that wraps the whole application for better logging.
## Setup
For testing, use this JWT token - 
```
Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc3NTMwMzE5OCwianRpIjoiMzdkNWI1OTctZjA5MS00NWE1LTlmMWYtYzkxYzQ1OWQ4NWQ4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjU0N2MxZjY1LWViZjgtNDdjOC1iNGQ1LTA2ZjNlYjM3ZWU1ZCIsIm5iZiI6MTc3NTMwMzE5OCwiY3NyZiI6IjU1YmYzZGE5LTBkNjktNGEyZi1hNTg1LWZlYmU3ZTM5ZmIzNSIsImV4cCI6MTc3NzAzMTE5OH0.VHl8B-tYNLPBHSybP7Fh2mN_NwcslMsw5_r4R-Ov4EA
```

**1. Clone and install dependencies**
```bash
git clone <repo-url>
cd zorvyn
pip install -r requirements.txt
```

**2. Configure environment**
```bash
cp env_example .env
```
as for this example, env_example contains all the keys that is use to run this backend.


**3. Run the server**
```bash
python3 server.py
```

For running it via docker, Dockerfile is already present
```bash
docker buildx build -t zorvyn .
docker run -d -p 3000:3000 --env-file=.env zorvyn:latest
```
 **All API's are avaiable in ```http://localhost:3000/docs```

