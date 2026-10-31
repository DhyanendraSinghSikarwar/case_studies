FROM python:3.12-slim
ENV DB_PASSWORD=Sup3rS3cretPw
ARG API_KEY=FAKE-abcdef123456
ARG AWS_ACCESS_KEY_ID=AKIAFAKEFAKEFAKE1234
ENV MODEL_URI=s3://ml-data/models/m1/
ENV DB_PASSWORD_FILE=/run/secrets/db_password
RUN pip install -r requirements.txt
