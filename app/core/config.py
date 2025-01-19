from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    DATABASE_NAME: str = Field(default=None)
    DATABASE_USER: str = Field(default=None)
    DATABASE_PASSWORD: str = Field(default=None)
    DATABASE_HOST: str = Field(default=None)
    DATABASE_PORT: int = None
    SECRET_KEY: str = Field(default=None)
    ALGORITHM: str = Field(default=None)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=None)
    REFRESH_TOKEN_EXPIRE_MINUTES: int = Field(default=None)
    

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra='ignore'
    )


settings = Settings()


