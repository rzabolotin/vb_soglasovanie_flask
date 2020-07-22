FROM python:3.8.3

RUN apt-get update -y && apt-get upgrade -y && apt-get autoremove && apt-get autoclean

COPY requirements.txt /etc/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r /etc/requirements.txt

CMD ["gunicorn", "--bind=0.0.0.0:80", "-w", "4", "webapp.wsgi:app"]
