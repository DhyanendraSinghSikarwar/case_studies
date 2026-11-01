# Option A: plain python-slim + PyTorch pip wheel (wheel bundles its CUDA user-space libs).
# Host still needs the NVIDIA driver and the NVIDIA Container Toolkit.
FROM python:3.11-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 \
    NVIDIA_VISIBLE_DEVICES=all NVIDIA_DRIVER_CAPABILITIES=compute,utility
WORKDIR /app
COPY requirements.txt .
# The default PyPI torch wheel for Linux is CUDA-enabled; to pin a CUDA flavour use the matching
# --index-url from the PyTorch install page (check current docs for the exact cuXXX tag).
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ src/
RUN useradd --uid 10001 app
USER 10001
EXPOSE 8000
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
