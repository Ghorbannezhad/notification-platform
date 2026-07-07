from sqlmodel import SQLModel, create_engine

from services.config import config
from services.database import models  # noqa: F401


engine = create_engine(config.database_url, echo=config.db_echo)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_and_tables()
