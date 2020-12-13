FROM tiangolo/uwsgi-nginx-flask:python3.6

#ADD odbcinst.ini /etc/odbcinst.ini

RUN apt-get update && apt-get install -y gcc unixodbc-dev
RUN apt-get update
RUN apt-get install -y tdsodbc unixodbc-dev
RUN apt install unixodbc-bin -y
RUN apt-get clean -y

COPY . /app

WORKDIR /app
#RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt --proxy=10.49.0.50:8080
RUN pip install -r requirements.txt 

EXPOSE 5000
#EXPOSE 1433

CMD ["python", "run.py"]
