ARG PY_VERSION=3.12
FROM python:${PY_VERSION}-slim AS builder
ARG PIP_INDEX_URL=https://pypi.org/simple
ARG GIT_SHA=unknown
RUN echo "index is $PIP_INDEX_URL, sha is $GIT_SHA"

FROM python:${PY_VERSION}-slim
ARG GIT_SHA
ENV MODEL_PATH=/models/churn.pkl \
    THRESHOLD=0.5 \
    BUILD_SHA=${GIT_SHA}
LABEL org.opencontainers.image.revision="${GIT_SHA}"
ARG PY_VERSION
RUN echo "python is ${PY_VERSION}"
CMD ["python", "-c", "import os; print(os.environ['MODEL_PATH'], os.environ['THRESHOLD'])"]
