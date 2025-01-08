from dotenv import load_dotenv
import os
from pydantic_settings import BaseSettings
from pathlib import Path

# Define the path to the .env file in the root directory
ENV_PATH = Path(__file__).resolve().parent.parent.parent / ".env"

# Load the .env file
load_dotenv(dotenv_path=ENV_PATH)

class Settings(BaseSettings):
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    STORAGE_PATH: str = "agents.json"
    KNOWLEDGE_BASE_PATH: str = "agent_knowledge"

    class Config:
        env_file = str(ENV_PATH)

settings = Settings()
