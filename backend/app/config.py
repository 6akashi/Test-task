from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Test Task Log"
    debug: bool = True
    database_url: str = 'sqllite:///./test_task.db'

    class Config:
        env_file = '.env'


settings = Settings()
