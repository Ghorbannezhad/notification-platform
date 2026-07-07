# Notification Platform

FastAPI service for a notification platform. The project uses PostgreSQL for
storage, SQLModel for models, and Alembic for database migrations.

## Requirements

- Docker and Docker Compose for the recommended startup path
- Python 3.11 if running the app locally

## Environment

Create a local `.env` file from the example:

```bash
cp .env.example .env
```

Default values:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=notification_db
DB_HOST=localhost
DB_PORT=5432
DB_PORT_EXPOSE=5439
DB_ECHO=false
```

`DB_PORT` is the PostgreSQL port used by the application. In Docker Compose,
the FastAPI container overrides `DB_HOST=postgres` and `DB_PORT=5432` because it
connects to Postgres inside the Docker network. `DB_PORT_EXPOSE` is the host
port exposed on your machine.

## Start With Docker

Build and start all services:

```bash
docker compose up --build
```

Run in the background:

```bash
docker compose up --build -d
```

Check the API:

```bash
curl http://localhost:8000/health
```

Useful service URLs:

- API: `http://localhost:8000`
- PgAdmin: `http://localhost:5050`
- RabbitMQ Management: `http://localhost:15672`
- PostgreSQL from host: `localhost:${DB_PORT_EXPOSE}`

Stop services:

```bash
docker compose down
```

Stop services and remove volumes:

```bash
docker compose down -v
```

## Database Migrations

Migrations are managed by Alembic.

When the FastAPI app starts, it runs:

```python
run_pending_migrations()
```

from:

```text
services/database/migrations.py
```

That function calls Alembic `upgrade head`, so only migrations that have not
already been applied are executed. Alembic tracks applied revisions in the
`alembic_version` table.

## Run Migrations Manually

If the Docker services are running, execute migrations inside the FastAPI
container:

```bash
docker compose exec fastapi python -m services.database.migrations
```

You can also call Alembic directly:

```bash
docker compose exec fastapi alembic upgrade head
```

For local execution, install dependencies first:

```bash
pip install -r requirements.txt
```

Then make sure `.env` points to a reachable database and run:

```bash
python -m services.database.migrations
```

or:

```bash
alembic upgrade head
```

## Create A New Migration

After changing SQLModel models, generate a migration:

```bash
alembic revision --autogenerate -m "describe change"
```

Review the generated file under `migrations/versions/`, then apply it:

```bash
python -m services.database.migrations
```

## Run The API Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Start only the backing services:

```bash
docker compose up -d postgres rabbitmq redis
```

Run the API from the project root:

```bash
uvicorn services.api.main:app --host 0.0.0.0 --port 8000 --reload
```

The app will run pending migrations during startup.

## Project Structure

```text
services/api/main.py              FastAPI app entrypoint
services/config.py                Environment configuration
services/database/models.py       SQLModel table models
services/database/migrations.py   Programmatic migration runner
migrations/env.py                 Alembic environment
migrations/versions/              Alembic migration files
```

`services/database/main.py` contains a direct `create_db_and_tables()` helper,
but normal database changes should go through Alembic migrations instead.
