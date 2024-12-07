from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    api_version: str = "v1"

    stage: str
    sqlalchemy_database_uri: str
    api_host: str

    magic_secret_key: str
    access_secret_key: str
    refresh_secret_key: str

    magic_token_expire_minutes: int = 15
    access_token_expire_minutes: int = 60
    refresh_token_expire_minutes: int = 60 * 24 * 7

    algorithm: str
    backend_cors_origins: str

    limiter_requests_per_second: int = 5

    email_port: int
    email_interface: int
    email_server: str

    frontend_host: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
