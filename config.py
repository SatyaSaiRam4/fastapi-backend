# config.py: Load environment variables using dotenv
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Retrieve credentials from environment
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

def validate_env_vars():
	missing = []
	for var in ["DB_NAME", "DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT"]:
		if not os.getenv(var):
			missing.append(var)
	if missing:
		raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")

# Validate on import
validate_env_vars()
