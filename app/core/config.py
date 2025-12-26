from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class KafkaConfig(BaseSettings):
    servers: str = "coffee_auth_kafka:9092"


class DatabaseConfig(BaseSettings):
    host: str = "coffee_auth_db"
    port: int = 5432
    name: str = "postgres"
    user: str = "postgres"
    password: str = "postgres"

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    @property
    def sync_url(self) -> str:
        return f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

class ApiConfig(BaseSettings):
    prefix: str = "/api/v1"


class Settings(BaseSettings):
    db: DatabaseConfig = DatabaseConfig()
    api: ApiConfig = ApiConfig()
    kafka: KafkaConfig = KafkaConfig()

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__"
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
