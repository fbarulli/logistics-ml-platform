from dataclasses import dataclass
import os


@dataclass(frozen=True)
class DatabaseConfig:

    url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://logistics:logistics@postgres:5432/logistics",
    )


database = DatabaseConfig()
