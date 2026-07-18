from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv

load_dotenv()


def required_env_var(name: str) -> str:
    value = getenv(name)

    if not value:
        error = f"A variavel de ambiente {name!r} não foi configurada"
        raise RuntimeError(error)

    return value


@dataclass
class Settings:
    mongo_uri: str
    mongo_database: str
    mongo_collection: str


def load_settings() -> Settings:
    return Settings(
        mongo_uri=getenv(
            "MONGO_URI",
            "mongodb://localhost:27017",
        ),
        mongo_database=required_env_var("MONGO_DATABASE"),
        mongo_collection=required_env_var("MONGO_COLLECTION"),
    )
