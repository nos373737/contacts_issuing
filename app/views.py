import pyodbc
from app import app
from flask import request, render_template, url_for
from app.models import User, ContactNumber, SapNumber, BaysQueue
from queue import Queue
 

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
q = Queue()
bays_all = BaysQueue.query.all()
for el in bays_all:
        q.put(el)

@app.route('/')
def homepage():
        return render_template('base.html')

@app.route('/check-contacts-for-sap-number', methods=('GET', 'POST'))
def check_contacts_post():
        if request.method == 'POST':
                text = request.form['text']
                search_result = SapNumber.query.filter_by(sap_number = text).first()
                return render_template('check.html', search_result=search_result)
        return render_template('check.html', search_result=None)

@app.route('/user-list')
def db_config():
        bays_list = list(q.queue)
        return render_template('users.html', bays_list=bays_list)
        #return str([(u.id, u.username, u.email) for u in User.query.all()])
        
@app.route('/check-bays')
def get_el_from_queue():
        result = q.get_nowait()
        return render_template('users.html', result=result)

@app.route('/numbers')
def numbers_list():
        numbers = ContactNumber.query.all()
        return render_template('contacts_list.html', numbers = numbers)

@app.route('/sap-numbers')
def sap_numbers_list():
        numbers = SapNumber.query.all()
        return render_template('sap_number_list.html', numbers = numbers)