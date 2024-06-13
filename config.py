import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('CSRF_KEY')
    MY_EMAIL = os.environ.get('MY_EMAIL')
    RECIPIENT_NAME = os.environ.get('RECIPIENT_NAME')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')
    CAPTCHA_PUBLIC_KEY = os.environ.get('CAPTCHA_PUBLIC_KEY')
    CAPTCHA_SECRET_KEY = os.environ.get('CAPTCHA_SECRET_KEY')
