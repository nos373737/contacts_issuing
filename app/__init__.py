# coding: utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

app.config.from_object("config")

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


from app import views
from app.views import User

from .views import main as main_blueprint
app.register_blueprint(main_blueprint)

# blueprint for auth routes in our app
from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from .models import User

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))
