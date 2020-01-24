from app import app
from . import db
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.ext.sqlalchemy.orm import model_form
from wtforms.validators import DataRequired
from wtforms.fields import DateTimeField, StringField
from wtforms import Form
from flask_wtf import FlaskForm 
from app.models import History, SapNumber, StatusEnum

# def all_sap_numbers():
#     return db.session.query(SapNumber).all()

# def all_status():
#     return db.session.query(StatusEnum).all()

# def all_available_contacts():
#     return db.session.query(SapNumber).filter()

# class HistoryForm(FlaskForm):
#     sap_number = QuerySelectField(query_factory=all_sap_numbers, allow_blank=True)
#     dpn = QuerySelectField(allow_blank=True)
#     serial_number = StringField(("Serial Number"), id="serial-number")
#     created_date  = DateTimeField(format='%Y-%m-%d %H:%M:%S')
#     status = QuerySelectField(query_factory=all_status, allow_blank=True)
HistoryTest = model_form(History, db_session=db.session)

class HistoryForm(FlaskForm):
    sap_number = QuerySelectField(allow_blank=True)
    dpn = QuerySelectField(allow_blank=True)
    serial_number = StringField(("Serial Number"), id="serial-number")
    created_date  = DateTimeField(format='%Y-%m-%d %H:%M:%S')
    status = QuerySelectField(allow_blank=True)
