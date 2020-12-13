# coding: utf-8
import datetime, enum, os, secrets
from PIL import Image
from app import app
from flask import request, render_template, url_for, redirect, flash, session
from app.models import User, ContactNumber, SapNumber, History, StatusEnum, Return, ReturnStatus, DPN
from app.forms import HistoryForm, ReturnForm, UpdateAccountImage, AddSapForm
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

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/css/images', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountImage()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        db.session.commit()
        flash('Your account image has been updated!', 'success')
        return redirect(url_for('main.profile'))
    image_file = url_for('static', filename='css/images/' + current_user.image_file)
    return render_template('profile.html', title='Account', image_file=image_file, form=form, name=current_user.username, current_user=current_user)

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
                flash("Бухта видана успішно!", 'success')
                return redirect(url_for('main.issuing_bays'))
        return render_template('history.html', form=form)

@main.route('/issued-bays-list')
@login_required
def issued_bays_list():
        page = request.args.get('page', 1, type=int)
        issued_bays = History.query\
                .order_by(History.create_date.desc())\
                .paginate(page=page, per_page=20)
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
        page = request.args.get('page', 1, type=int)
        history = Return.query\
                .order_by(Return.create_date.desc())\
                .paginate(page=page, per_page=20)
        return render_template('return_history.html', history = history)

@main.route('/active-return')
@login_required
def active_return():
        page = request.args.get('page', 1, type=int)
        active = Return.query\
                .filter_by(status = ReturnStatus.new)\
                .order_by(Return.create_date.desc())\
                .paginate(page=page, per_page=20)
        return render_template('active_return.html', active = active)

@main.route('/add-sap', methods=['GET', 'POST'])
@login_required
def add_sap():
        form = AddSapForm()
        if request.method == 'POST' and form.validate_on_submit():
                dpn_list = request.form.getlist('dpn_first')
                sap_num = SapNumber(sap_number = request.form.get('sp_num'))
                for el in dpn_list:
                        dpn = DPN.query.filter_by(id = el).first()
                        contact = ContactNumber(description = dpn.dpn)
                        sap_num.contacts.append(contact) 
                db.session.add(sap_num)
                db.session.commit()
                flash("SAP № з контактами додано успішно!", 'success')
                return redirect(url_for('main.add_sap'))
        return render_template('add_sap.html', form = form)