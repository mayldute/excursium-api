# Excursium Backend

Excursium is a modular asynchronous FastAPI backend for a passenger transport
marketplace. It supports clients, carriers, vehicles, routes, schedules,
authentication, OAuth, file storage, and scheduled cleanup jobs.

The project began during a hackathon and was later refactored into a
portfolio-ready modular application.

## Architecture

The codebase uses vertical feature modules. Each business domain owns its API,
schemas, and business logic, while shared technical integrations live under
`infrastructure`.

```text
app/
├── core/
│   ├── config.py
│   ├── exception_handlers.py
│   ├── exceptions.py
│   ├── security.py
│   └── tokens.py
├── infrastructure/
│   ├── database/
│   │   ├── models/
│   │   ├── base.py
│   │   └── session.py
│   ├── email/
│   ├── oauth/
│   └── storage/
├── modules/
│   ├── auth/
│   │   ├── router.py
│   │   ├── schemas.py
│   │   └── service.py
│   ├── clients/
│   ├── carriers/
│   └── transports/
├── shared/
│   ├── constants.py
│   ├── dependencies.py
│   └── validators.py
├── tasks/
└── main.py
```

## Why This Structure

- Feature code is grouped by business domain.
- Infrastructure integrations do not live in a generic `utils` directory.
- Authentication dependencies are centralized.
- FastAPI application creation is isolated in `create_application()`.
- Scheduled jobs start and stop through the application lifespan.
- ORM models and database configuration are clearly separated.
- Compatibility facades preserve existing imports during gradual refactoring.

## Features

- Client and carrier registration
- Individual and legal-entity validation
- JWT access and refresh tokens
- Email activation and email changes
- Google and Yandex OAuth
- MinIO file storage
- Transport CRUD
- Routes, prices, schedules, and availability search
- Soft deletion
- Scheduled cleanup tasks
- Async SQLAlchemy and PostgreSQL
- Alembic migrations
- OpenAPI documentation

## Installation

```bash
uv sync --extra dev
cp .env.example .env
```

Generate a JWT secret:

```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

## Infrastructure

```bash
docker compose up -d postgres minio
```

MinIO console:

```text
http://127.0.0.1:9001
```

## Migrations

```bash
uv run alembic revision --autogenerate -m "create initial tables"
uv run alembic upgrade head
```

## Run

```bash
uv run uvicorn app.main:app --reload --reload-dir app
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## Tests and Code Quality

```bash
uv run pytest
uv run ruff format .
uv run ruff check . --fix
```

## Environment Files

The repository contains a complete `.env.example`. Copy it to `.env` and
replace placeholders with local credentials. Never commit `.env`.

## Scope Note

The supplied project referenced future `Order` and `Comment` domains, but
their implementations were not included in the uploaded files. Unresolved ORM
relationships to those missing domains are not part of this prepared version.
They should be implemented as separate vertical modules.
