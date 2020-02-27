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
from app.models import History, SapNumber, StatusEnum

def all_sap_numbers():
    return db.session.query(SapNumber).all()

class HistoryForm(FlaskForm):
    sap_number = QuerySelectField(query_factory=all_sap_numbers, allow_blank=True)
    dpn = StringField(("DPN"), id="dpn")
    serial_number = StringField(("Serial Number"), id="serial-number")
    status = SelectField('Status', [DataRequired()],
                        choices=[(StatusEnum.ok, 'OK'), (StatusEnum.nok, 'NOK')])

# HistoryTest = model_form(History, db_session=db.session)

