FROM python:3.9-slim-buster

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV VAULT_ADDR="http://vault.tchowdhury.org"

EXPOSE 6000

CMD ["python", "manutd.py"]