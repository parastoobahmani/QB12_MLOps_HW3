FROM python:3.11-slim AS builder
WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip &&     pip install --target=/install -r requirements.txt

FROM python:3.11-slim

WORKDIR /app

ENV PYTHONPATH=/app:/install

COPY --from=builder /install /install
COPY src/ src/
COPY pyproject.toml .

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "src.airbnb_serving.app:app", "--host", "0.0.0.0", "--port", "8000"]