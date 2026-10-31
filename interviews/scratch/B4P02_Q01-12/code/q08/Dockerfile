# The digest below is a PLACEHOLDER for illustration; get the real one from your registry
# (e.g. `docker buildx imagetools inspect python:3.11-slim-bookworm`) and let a bot bump it.
FROM python:3.11-slim-bookworm@sha256:0000000000000000000000000000000000000000000000000000000000000000
ARG SOURCE_DATE_EPOCH
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --require-hashes -r requirements.txt
COPY src/ src/
CMD ["python", "-m", "src.serve"]
