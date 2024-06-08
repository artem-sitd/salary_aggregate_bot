import os

from dotenv import load_dotenv

env_file = ".env.docker" if os.getenv("USE_DOCKER") else ".env"
load_dotenv(env_file)

load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
MONGO_URL = os.getenv("MONGO_URL")
