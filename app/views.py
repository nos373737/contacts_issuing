import pyodbc
from app import app
from flask import render_template, url_for
from app.models import User, NumberContacts

@app.route('/')
def hello_world():
    conn = pyodbc.connect('Driver={SQL Server};' 'Server=UACVDB01\SQL2008EXPRESS;' 'Database=bays_contacts;' 'Trusted_Connection=no;' 'UID=snadmin;' 'PWD=sysadmin;')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bays_contacts.dbo.test')
    res = []
    for row in cursor:
            res.append(row)    
    return str(res)

@app.route('/user-list')
def db_config():
        users = User.query.all()
        return render_template('index.html', name = 'PRETTL AEU', users = users)
        #return str([(u.id, u.username, u.email) for u in User.query.all()])
        
