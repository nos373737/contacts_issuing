import pyodbc, datetime, enum
from app import app
from flask import request, render_template, url_for, redirect, flash, session
from app.models import User, ContactNumber, SapNumber, History, StatusEnum, Return, ReturnStatus
from queue import Queue
from app.forms import HistoryForm, ReturnForm
from wtforms.validators import ValidationError
from . import db, login_manager
from flask import Blueprint
from flask_login import login_required, current_user

# @app.route('/')
# def hello_world():
#     conn = pyodbc.connect('Driver={FreeTDS};' 'Server=UACVDB01\SQL2008EXPRESS;' 'Database=bays_contacts;' 'Trusted_Connection=no;' 'UID=snadmin;' 'PWD=sysadmin;')
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM bays_contacts.dbo.history')
#     res = []
#     for row in cursor:
#             res.append(row)    
#     return str(res)

main = Blueprint('main', __name__)

@main.route('/')
def homepage():
        return render_template('base.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.username)

@main.route('/check-contacts-for-sap-number', methods=('GET', 'POST'))
@login_required
def check_contacts_post():
        if request.method == 'POST':
                text = request.form['search_sap']
                search_result = SapNumber.query.filter_by(sap_number = text).first()
                return render_template('check.html', search_result=search_result)
        return render_template('check.html', search_result=None)

# @app.route('/user-list')
# def db_config():
#         bays_list = list(q.queue)
#         return render_template('users.html', bays_list=bays_list)
#         #return str([(u.id, u.username, u.email) for u in User.query.all()])


@main.route('/numbers')
def numbers_list():
        numbers = ContactNumber.query.all()
        return render_template('contacts_list.html', numbers = numbers)

@main.route('/sap-numbers')
def sap_numbers_list():
        numbers = SapNumber.query.all()
        return render_template('sap_number_list.html', numbers = numbers)

# Route for adding record that operator get bays
@main.route('/bays-issuing', methods=['GET', 'POST'])
@login_required
def issuing_bays():
        # Initialized form for bays issuing
        form = HistoryForm()
        if request.method == 'POST' and form.validate_on_submit():
                sap = SapNumber.query.filter_by(sap_number = request.form.get("sap_number")).all()
                for el in sap:
                        sap_id = el.id
                History.create(sap_number=sap_id,
                dpn = request.form.get("dpn"),
                serial_number = request.form.get("serial_number"),
                status = StatusEnum.ok)
                flash("Бухта додана успішно!", 'info')
                return redirect(url_for('main.issuing_bays'))
        return render_template('history.html', form=form)

@main.route('/issued-bays-list')
@login_required
def issued_bays_list():
        issued_bays = History.query.all()
        return render_template('issued_bays_list.html', issued_bays = issued_bays)

@main.route('/bays-return', methods=['GET', 'POST'])
@login_required
def bays_return():
        form = ReturnForm()
        if request.method == 'POST' and form.validate_on_submit():
                record = Return(dpn=request.form.get("dpn"),
                serial_number=request.form.get("serial_number"),
                status=ReturnStatus.new,
                create_date=datetime.datetime.now())
                db.session.add(record)
                db.session.commit()
                flash("Бухта повернена успішно!", 'info')
                return redirect(url_for('main.bays_return'))
        return render_template('return.html', form=form)

@main.route('/return-history')
@login_required
def return_history():
        history = Return.query.all()
        return render_template('return_history.html', history = history)

@main.route('/active-return')
@login_required
def active_return():
        active = Return.query.filter_by(status = ReturnStatus.new).all()
        return render_template('active_return.html', active = active)