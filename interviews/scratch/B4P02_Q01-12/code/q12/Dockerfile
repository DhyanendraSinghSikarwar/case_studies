FROM python:3.11-slim-bookworm
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ src/
COPY healthcheck.py .
RUN useradd --uid 10001 app
USER 10001
EXPOSE 8000
# start-period: failures during the first 120 s do not count toward retries (model loads ~90 s)
HEALTHCHECK --interval=15s --timeout=3s --start-period=120s --retries=3 \
  CMD ["python", "/app/healthcheck.py", "http://127.0.0.1:8000/ready"]
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
