FROM tiangolo/uwsgi-nginx-flask:python3.6

# install FreeTDS and dependencies
RUN apt-get update \
 && apt-get install unixodbc -y \
 && apt-get install unixodbc-dev -y \
 && apt-get install freetds-dev -y \
 && apt-get install freetds-bin -y \
 && apt-get install tdsodbc -y \
 && apt-get install --reinstall build-essential -y
RUN echo "[FreeTDS]\n\
Description = FreeTDS unixODBC Driver\n\
Driver = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so\n\
Setup = /usr/lib/x86_64-linux-gnu/odbc/libtdsS.so" >> /etc/odbcinst.ini


COPY . /app

WORKDIR /app
#RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt --proxy=10.49.0.50:8080
RUN pip install -r requirements.txt 

EXPOSE 5000

CMD ["python", "run.py"]

