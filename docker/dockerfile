FROM python:3.9

WORKDIR /app

COPY python/ .

RUN pip install -r requirements.txt

CMD ["python", "populateDB.py"]