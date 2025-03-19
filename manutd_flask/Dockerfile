FROM python:3.9-slim-buster

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV VAULT_ADDR="http://192.168.68.56:8200/"

EXPOSE 5000

CMD ["python", "manutd.py"]