from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_core import MultiHostUrl
from pydantic import (
    PostgresDsn,
    computed_field,
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    api_version: str = "v1"

    stage: str

    pg_container_name: str
    pg_user: str
    pg_password: str
    pg_db: str
    pg_port: int
    pg_host: str

    @computed_field  # type: ignore[prop-decorator]
    @property
    def sqlalchemy_database_uri(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg2",
            username=self.pg_user,
            password=self.pg_password,
            # when using compose due to internal network
            host=self.pg_container_name,
            # host=self.pg_host,
            # port=self.pg_port,
            path=self.pg_db,
        )

    api_host: str
    api_port: int

    magic_secret_key: str
    access_secret_key: str
    refresh_secret_key: str

    magic_token_expire_minutes: int = 15
    access_token_expire_minutes: int = 60
    refresh_token_expire_minutes: int = 60 * 24 * 7

    algorithm: str
    cors_list: str

    @computed_field  # type: ignore[prop-decorator]
    @property
    def backend_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.cors_list.split(",")] + [
            self.frontend_host
        ]

    limiter_requests_per_second: int = 5

    email_container_name: str
    email_port: int
    email_interface: int
    email_server: str

    frontend_host: str


settings = Settings()
