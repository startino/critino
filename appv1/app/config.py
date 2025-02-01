from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv(".env") 

class Settings(BaseSettings):
    google_api_key: str
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()