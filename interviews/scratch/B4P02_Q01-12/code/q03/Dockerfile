# syntax=docker/dockerfile:1
FROM python:3.11-slim-bookworm AS builder
# hadolint ignore=DL3008
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libgomp1 \
    && rm -rf /var/lib/apt/lists/*
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM builder AS test
COPY tests/ /app/tests/
COPY src/ /app/src/
RUN pip install --no-cache-dir pytest==8.3.3 && python -m pytest -q tests

FROM python:3.11-slim-bookworm AS runtime
# hadolint ignore=DL3008
RUN apt-get update \
    && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --uid 10001 --create-home app
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
COPY --chown=app:app src/ /app/src/
USER 10001
CMD ["python", "-m", "src.serve"]
