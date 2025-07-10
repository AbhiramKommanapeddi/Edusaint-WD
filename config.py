import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration class"""
    
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    
    # Database configuration
    DB_CONFIG = {
        'host': os.environ.get('DB_HOST') or 'localhost',
        'user': os.environ.get('DB_USER') or 'root',
        'password': os.environ.get('DB_PASSWORD') or '',
        'database': os.environ.get('DB_NAME') or 'school_reviews',
        'port': int(os.environ.get('DB_PORT', 3306)),
        'charset': 'utf8mb4',
        'autocommit': True
    }