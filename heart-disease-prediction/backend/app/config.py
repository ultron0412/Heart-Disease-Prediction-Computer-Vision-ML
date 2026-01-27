from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Heart Disease Prediction"
    DEBUG: bool = True

settings = Settings()
