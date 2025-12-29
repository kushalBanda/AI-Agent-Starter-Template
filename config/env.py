# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


class Environment():

    # General
    ENV = os.getenv("ENV")
    PRODUCT_NAME = os.getenv("PRODUCT_NAME")
    APP_URL = os.getenv("APP_URL")
    LANDING_URL = os.getenv("LANDING_URL")
    
    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL")

    # Anthropic
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL")

    # GitHub
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    GITHUB_BASE_URL = os.getenv("GITHUB_BASE_URL")