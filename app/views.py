import pyodbc, datetime, enum
from app import app
from flask import request, render_template, url_for, redirect, flash, session
from app.models import User, ContactNumber, SapNumber, History, StatusEnum, Return, ReturnStatus
from queue import Queue
from app.forms import HistoryForm, ReturnForm
from . import db
 

# @app.route('/')
# def hello_world():
#     conn = pyodbc.connect('Driver={SQL Server};' 'Server=UACVDB01\SQL2008EXPRESS;' 'Database=bays_contacts;' 'Trusted_Connection=no;' 'UID=snadmin;' 'PWD=sysadmin;')
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM bays_contacts.dbo.test')
#     res = []
#     for row in cursor:
#             res.append(row)    
#     return str(res)

#Get the value of bays thatfrom db
# q = Queue()
# bays_all = BaysQueue.query.all()
# for el in bays_all:
#         q.put(el)


@app.route('/')
def homepage():
        return render_template('base.html')

@app.route('/check-contacts-for-sap-number', methods=('GET', 'POST'))
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
        
# @app.route('/check-bays')
# def get_el_from_queue():
#         result = q.get_nowait()
#         return render_template('users.html', result=result)

@app.route('/numbers')
def numbers_list():
        numbers = ContactNumber.query.all()
        return render_template('contacts_list.html', numbers = numbers)

@app.route('/sap-numbers')
def sap_numbers_list():
        numbers = SapNumber.query.all()
        return render_template('sap_number_list.html', numbers = numbers)

# Route for adding record that operator get bays
@app.route('/bays-issuing', methods=['GET', 'POST'])
def issuing_bays():
        # Initialized form for bays issuing
        form = HistoryForm()
        if request.method == 'POST' and form.validate_on_submit():
                sap_number = request.form.get("sap_number")
                dpn = request.form.get("dpn")
                check_result = check_dpn(sap_number, dpn)
                sap = SapNumber.query.filter_by(id = int(sap_number)).all()
                contacts = ContactNumber.query.filter_by(sap_num_id=int(sap_number)).all()
                if check_result != StatusEnum.ok:
                        flash(u"Try enter another DPN!!! This DPN not relevant for Sap Number:" \
                                + str(sap) \
                                + "For this Sap Number you need this contacts:" \
                                + str(contacts), 'error')
                else:
                        dpn_check_res = has_history_dpn(dpn, sap_number,
                                request.form.get("serial_number"),
                                check_result)
                        if dpn_check_res != True:
                                session["formdata"] = {"sap_number" : sap_number, "dpn" : dpn}
                                return redirect(url_for('issuing_bays'))
                return redirect(url_for('issuing_bays'))
        return render_template('history.html', form=form)

# Check if contacts(DPN) relevant to SapNumber
def check_dpn(sap_id, dpn):
        available_contacts = ContactNumber.query.filter_by(sap_num_id=sap_id).all()
        for el in available_contacts:
                if (str(el) == str(dpn)):
                        return StatusEnum.ok
        return StatusEnum.nok

def has_history_dpn(dpn, sap_number, serial_number, status):
        check_dpn = Return.query.filter_by(dpn=dpn, status=ReturnStatus.new).first()
        if check_dpn != None and check_dpn.serial_number != serial_number:
                flash(u"Bays for this contacts available from return list!" \
                        + "Please get bays with serial number:" \
                        + str(check_dpn.serial_number), 'error')
                return False
        else:
                History.create(sap_number=sap_number,
                                dpn=dpn,
                                serial_number=serial_number,
                                status=status)
                if check_dpn != None:
                        check_dpn.status = ReturnStatus.recycled
                        db.session.commit()
                return True

@app.route('/issued-bays-list')
def issued_bays_list():
        issued_bays = History.query.all()
        return render_template('issued_bays_list.html', issued_bays = issued_bays)

@app.route('/bays-return', methods=['GET', 'POST'])
def bays_return():
        form = ReturnForm()
        if request.method == 'POST':
                serial_number = request.form.get("serial_number")
                dpn = request.form.get("dpn")
                if ContactNumber.query.filter_by(description=dpn).first() == None:
                        flash(u"Not correct DPN! Please check it!", 'error')
                else:
                        record = Return(dpn=dpn, serial_number=serial_number, status=ReturnStatus.new, create_date=datetime.datetime.now())
                        db.session.add(record)
                        db.session.commit()
                return redirect(url_for('bays_return'))

        return render_template('return.html', form=form)
