import os
from pathlib import Path
from dotenv import load_dotenv

# Get the root directory (parent of lib directory)
ROOT_DIR = Path(__file__).parent.parent

# Load environment variables from .env file in root directory
env_path = ROOT_DIR / ".env"
load_dotenv(env_path)

# Export commonly used environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")
LANGFUSE_HOST = os.getenv("LANGFUSE_HOST")
