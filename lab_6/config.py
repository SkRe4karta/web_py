import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

# Базовые настройки
SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

# Настройки базы данных
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Настройки загрузки файлов
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'images')
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

# Создаем папку для загрузок, если её нет
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
