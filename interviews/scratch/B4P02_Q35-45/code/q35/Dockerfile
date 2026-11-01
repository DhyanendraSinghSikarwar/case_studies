# syntax=docker/dockerfile:1
FROM python:3.12-slim AS base
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/

FROM base AS test
COPY requirements-test.txt .
RUN pip install --no-cache-dir -r requirements-test.txt
COPY tests/ ./tests/
ENV PYTHONPATH=/app/src
CMD ["pytest", "-q"]

FROM base AS final
ENV PYTHONPATH=/app/src
USER 10001
CMD ["python", "-m", "mlsvc"]
