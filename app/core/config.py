from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Room reservation system'

    class Config:
        env_file = '.env'


settings = Settings()
