import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
# Production default points to postgres service 'db' used in docker-compose or Render's managed Postgres
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+psycopg2://finan_user:finan_pass@db:5432/financontrol')
SECRET_KEY = os.getenv('SECRET_KEY', 'replace-this-with-a-very-secret-key')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 60*24*7))
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', str(BASE_DIR / 'uploads'))
