FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN pip install flask mysql-connector-python flask-wtf

CMD ["python", "app.py"]


