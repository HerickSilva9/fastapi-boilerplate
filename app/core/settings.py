"""Settings and Environment Variables"""
import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

all_cors_origins = str(os.getenv('BACKEND_CORS_ORIGINS')).split(',')