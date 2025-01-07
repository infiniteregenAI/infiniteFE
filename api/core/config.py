import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    STORAGE_PATH: str = "agents.json"
    KNOWLEDGE_BASE_PATH: str = "agent_knowledge"
    
    class Config:
        env_file = ".env"

settings = Settings()