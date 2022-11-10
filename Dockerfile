FROM python:3.11.0-alpine

EXPOSE 5000

WORKDIR /home/flask-api
COPY src/ .

RUN pip3 install -r requirements.txt

CMD ["python3", "./api.py"]
