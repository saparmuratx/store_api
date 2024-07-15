from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    TEST_DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRATION: int
    JWT_ALGORITHM: str


settings = Settings()
