FROM python:3.12-slim

WORKDIR /app

COPY producer/requirements.txt .

RUN pip install -r requirements.txt

COPY producer/producer.py .

COPY src/logistics_ml /app/logistics_ml

ENV PYTHONPATH=/app

CMD ["python", "producer.py"]
