import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    DEBUG = os.getenv('FLASK_ENV') == 'development'
    
    # Database settings
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 
                                      f"postgresql://{os.getenv('POSTGRES_USER', 'postgres')}:{os.getenv('POSTGRES_PASSWORD', 'secret')}@{os.getenv('POSTGRES_HOST', 'localhost')}:{os.getenv('POSTGRES_PORT', '5432')}/{os.getenv('POSTGRES_DB', 'genealogy_db')}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # CORS settings
    CORS_HEADERS = 'Content-Type'

    @staticmethod
    def build_db_uri(prefix="POSTGRES"):
        user = os.getenv(f"{prefix}_USER", "postgres")
        pw = os.getenv(f"{prefix}_PASSWORD", "")
        host = os.getenv(f"{prefix}_HOST", "localhost")
        port = os.getenv(f"{prefix}_PORT", "5432")
        db = os.getenv(f"{prefix}_DB", "postgres")
        return f"postgresql://{user}:{pw}@{host}:{port}/{db}"


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = Config.build_db_uri("POSTGRES")
    DEBUG = True


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = Config.build_db_uri("TEST_POSTGRES")
    TESTING = True
