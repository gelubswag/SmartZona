from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    SECRET: str
    DEBUG: bool

    # Postgres settings
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    class Config:
        env_file = ".env"


settings = Settings()

print(settings)
