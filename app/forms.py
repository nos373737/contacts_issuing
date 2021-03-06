#! /usr/bin/env python
# -*- coding: utf-8 -*-
from app import app
from . import db
from werkzeug.security import check_password_hash
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, InputRequired, ValidationError
from wtforms import (StringField,
                     TextAreaField,
                     SubmitField,
                     PasswordField,
                     DateTimeField,
                     SelectField,
                     Form)
from flask_wtf import FlaskForm 
from app.models import History, SapNumber, Return, ContactNumber, ReturnStatus, StatusEnum, User, DPN

# def all_sap_numbers():
#     return db.session.query(SapNumber).all()

#Validation for form fileds 
def my_length_check(form, field):
    if len(field.data) != 8:
        raise ValidationError(message = "Номер контакту повинен складатися з 8 цифр!")
#Checking the existing of Sap Number
def sap_check(form, field):
    sap_list = db.session.query(SapNumber).filter_by(sap_number = field.data).first()
    if sap_list == None:
        raise ValidationError(message = "Такий SAP-номер не існує! Зверніться до адміністратора!")

# Checking the relevant of dpn to sap number    
def check_dpn_to_sap(form, field):
        available_contacts = SapNumber.query.filter_by(sap_number=form.sap_number.data).all()
        print(available_contacts)
        if available_contacts == []:
            raise ValidationError(message = "Для неіснуючого Sap-номеру неможливо перевірити DPN(контакт)!")
        else:
            for el in available_contacts:
                if field.data not in str(el.contacts):
                    raise ValidationError(message = u"Спробуйте інший DPN!!! Цей DPN некоректний для Sap-номеру: " \
                                + form.sap_number.data \
                                + " Для цього Sap-номеру Вам потрібні контакти:" \
                                + str(el.contacts))
        

# Check if there was a history for dpn
def has_dpn_history(form, field):
        check_dpn = Return.query.filter_by(dpn=field.data, status=ReturnStatus.new).first()
        if check_dpn != None and check_dpn.serial_number != form.serial_number.data:
                raise ValidationError(message = u"Бухта для такого контакту(DPN) є в списку повернення!" \
                        + "Будь ласка, візміть бухту з серійним номером: " \
                        + str(check_dpn.serial_number))
        if check_dpn != None:
                        check_dpn.status = ReturnStatus.recycled
                        db.session.commit()

# Form for getting the bays by operator
class HistoryForm(FlaskForm):
    #sap_number = QuerySelectField("Sap Number", [InputRequired()], query_factory=all_sap_numbers, allow_blank=True)
    sap_number = StringField("Sap Number", [InputRequired(), sap_check])
    dpn = StringField(("DPN"), [InputRequired(), my_length_check, check_dpn_to_sap, has_dpn_history])
    serial_number = StringField(("Serial Number"), [InputRequired(),
    Length(9, 9, message="Серійний номер повинен складатись з 9 цифр!")],
    id="serial-number")
    status = SelectField(u'Status',
    choices=[(member.value, name.capitalize()) for name, member in StatusEnum.__members__.items()])

#Check dpn existing
def dpn_exist(form, field):
    if ContactNumber.query.filter_by(description=field.data).first() == None:
        raise ValidationError(message = u"Не коректний DPN! Будь ласка перевірте його!")

#Form for returning bays
#ReturnForm = model_form(Return)
class ReturnForm(FlaskForm):
    serial_number = StringField(("Serial Number"), [InputRequired(),
    Length(9, 9, message="Серійний номер повинен складатись з 9 цифр!")],
    id="serial-number")
    dpn = StringField(("DPN"), [InputRequired(), my_length_check, dpn_exist])
    status = SelectField(u'Status',
    choices=[(member.value, name.capitalize()) for name, member in ReturnStatus.__members__.items()])

# Validation for Login Form

def user_check(form, field):
    user = User.query.filter_by(username=field.data).first()
    if not user or not check_password_hash(user.password, form.password.data):
        raise ValidationError(message = u'Будь ласка перевірте авторизаційні дані! Невірний логін або пароль!')

# Login form

class LoginForm(FlaskForm):
    username = StringField(("Ім'я користувача"), [InputRequired(), user_check])
    password = PasswordField(("Пароль"), [InputRequired(),
    Length(8, message="Довжина паролю повинна складати мінімум 8 символів!")])

class UpdateAccountImage(FlaskForm):
    picture = FileField('Змінити зображення користувача', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Змінити')

def all_dpn():
        return db.session.query(DPN).all()

class AddSapForm(FlaskForm):
    sp_num = StringField(("Sap Number"), [InputRequired(),
    Length(8, 8, message="Довжина SAP № має складати 8 символів!")])
    dpn_first = QuerySelectMultipleField(("DPN List"), query_factory=all_dpn, allow_blank=False, validators=[InputRequired()])

    