import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from config import Config

PROD = True if os.environ.get('PROD', False) == 'True' else False

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
csrf = CSRFProtect(app)

@login.user_loader
def load_user(user_id):
    from models import User

    return User.query.get(int(user_id))

from routes import *

if __name__ == '__main__':
    app.run(debug=not PROD)
