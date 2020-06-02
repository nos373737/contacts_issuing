import urllib


#params = urllib.parse.quote_plus('DRIVER={SQL Server};SERVER=UACVDB01\SQL2008EXPRESS;DATABASE=bays_contacts;Trusted_Connection=no;UID=snadmin;PWD=sysadmin;')
params = urllib.parse.quote_plus('DRIVER={FreeTDS};SERVER=UACVDB01\SQL2008EXPRESS;PORT=1433;DATABASE=bays_contacts;Trusted_Connection=no;UID=snadmin;PWD=sysadmin;TDS_Version=8.0;')

SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % params
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'Flk;21331;4kdqaFTYe3'
# SQLALCHEMY_ENGINE_OPTIONS = {
#     'encoding': 'utf8' 
# }

