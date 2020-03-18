from app import app
from . import db
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.ext.sqlalchemy.orm import model_form
from wtforms.validators import DataRequired, Length
from wtforms import (StringField,
                     TextAreaField,
                     SubmitField,
                     PasswordField,
                     DateTimeField,
                     SelectField,
                     Form)
from flask_wtf import FlaskForm 
from app.models import History, SapNumber, StatusEnum, Return, ReturnStatus

def all_sap_numbers():
    return db.session.query(SapNumber).all()
    
# Form for geting the bays by operator
class HistoryForm(FlaskForm):
    sap_number = QuerySelectField(query_factory=all_sap_numbers, allow_blank=True)
    dpn = StringField(("DPN"), id="dpn")
    serial_number = StringField(("Serial Number"), id="serial-number")
    status = SelectField(u'Status', choices=[(member.value, name.capitalize()) for name, member in StatusEnum.__members__.items()])

ReturnForm = model_form(Return)
