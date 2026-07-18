FROM python:3.12-slim

WORKDIR /app

COPY consumer/requirements.txt .

RUN pip install -r requirements.txt

COPY consumer/consumer.py .

COPY src/logistics_ml /app/logistics_ml

ENV PYTHONPATH=/app

CMD ["python", "consumer.py"]
