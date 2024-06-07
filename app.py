import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from config import Config

PROD = True if os.environ.get('PROD', False) == 'True' else False

app = Flask(__name__)
app.config.from_object(Config)

csrf = CSRFProtect(app)

from routes import *

if __name__ == '__main__':
    app.run(debug=not PROD)
