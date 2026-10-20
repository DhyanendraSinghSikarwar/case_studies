FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN pip install --no-cache-dir -e . --no-deps
ENV PYTHONPATH=/app/src
EXPOSE 8501
# The app reads precomputed artifacts from outputs/ (commit them or run `python tasks.py train` first).
CMD ["streamlit", "run", "app/streamlit_app.py", "--server.address=0.0.0.0"]
