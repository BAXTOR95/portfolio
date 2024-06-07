import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('CSRF_KEY')
    MY_EMAIL = os.environ.get('MY_EMAIL')
    RECIPIENT_NAME = os.environ.get('RECIPIENT_NAME')
