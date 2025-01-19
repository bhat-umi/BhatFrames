from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    DATABASE_NAME: str = Field(default=None)
    DATABASE_USER: str = Field(default=None)
    DATABASE_PASSWORD: str = Field(default=None)
    DATABASE_HOST: str = Field(default=None)
    DATABASE_PORT: int = None
    

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra='ignore'
    )


settings = Settings()


