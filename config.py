# SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % params
# SQLALCHEMY_TRACK_MODIFICATIONS = False
import os


basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'Flk;21331;4kdqaFTYe3'
# SQLALCHEMY_ENGINE_OPTIONS = {
#     'encoding': 'utf8' 
# }