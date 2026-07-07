from pathlib import Path
from time import sleep

from alembic import command
from alembic.config import Config as AlembicConfig
from sqlalchemy.exc import OperationalError


BASE_DIR = Path(__file__).resolve().parents[2]
ALEMBIC_INI = BASE_DIR / "alembic.ini"
MAX_RETRIES = 30
RETRY_DELAY_SECONDS = 1


def run_pending_migrations() -> None:
    alembic_config = AlembicConfig(str(ALEMBIC_INI))
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            command.upgrade(alembic_config, "head")
            return
        except OperationalError:
            if attempt == MAX_RETRIES:
                raise
            sleep(RETRY_DELAY_SECONDS)


if __name__ == "__main__":
    run_pending_migrations()
