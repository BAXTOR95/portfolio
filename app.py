import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_sitemap import Sitemap
from config import Config
from datetime import date

PROD = True if os.environ.get('PROD', False) == 'True' else False

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
csrf = CSRFProtect(app)
ext = Sitemap(app=app)


@login.user_loader
def load_user(user_id):
    from models import User

    return User.query.get(int(user_id))


# Flask-Sitemap generators
@ext.register_generator
def index():
    yield 'index', {}, date.today(), 'monthly', 1.0


@ext.register_generator
def about():
    yield 'about', {}, date.today(), 'monthly', 0.8


@ext.register_generator
def contact():
    yield 'contact', {}, date.today(), 'monthly', 0.8


@ext.register_generator
def portfolio():
    yield 'portfolio', {}, date.today(), 'monthly', 0.8


@ext.register_generator
def resume():
    yield 'resume', {}, date.today(), 'monthly', 0.8


@ext.register_generator
def services():
    yield 'services', {}, date.today(), 'monthly', 0.8


# Add zip to Jinja2 environment globals
app.jinja_env.globals.update(zip=zip)

from routes import *

if __name__ == '__main__':
    app.run(debug=not PROD)
