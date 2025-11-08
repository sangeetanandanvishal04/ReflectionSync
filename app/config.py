from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    email: str
    smtp_password: str

    initial_admin_email: Optional[str] = None
    initial_admin_password: Optional[str] = None

    class Config:
        env_file = ".env"

settings = Settings()