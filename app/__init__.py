from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config.from_object("config")
app.config['SECRET_KEY'] = 'Flk;21331;4kdqaFTYe3'
db = SQLAlchemy(app)

from app import views
from app.views import User
