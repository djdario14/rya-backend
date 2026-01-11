import os

class Settings:
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'sqlite:///./test.db')
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'secret')
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()
