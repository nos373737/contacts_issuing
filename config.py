import urllib

params = urllib.parse.quote_plus('DRIVER={SQL Server};SERVER=UACVDB01\SQL2008EXPRESS;DATABASE=bays_contacts;Trusted_Connection=no;UID=snadmin;PWD=sysadmin;')

SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % params
SQLALCHEMY_TRACK_MODIFICATIONS = False
