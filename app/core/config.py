from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # These names must match the keys in your .env file
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # This tells Pydantic to look for a .env file
    model_config = SettingsConfigDict(env_file=".env")

# Create a single instance to be imported elsewhere
settings = Settings()