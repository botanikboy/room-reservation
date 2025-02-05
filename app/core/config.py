from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    app_title: str = 'Room reservation system'
    database_url: str
    secret: str = 'SECRET'
    base_dir: Path = Path(__file__).resolve().parent.parent
    templates_dir: Path = base_dir / 'templates'
    static_dir: Path = base_dir / 'static'

    class Config:
        env_file = '.env'


settings = Settings()
