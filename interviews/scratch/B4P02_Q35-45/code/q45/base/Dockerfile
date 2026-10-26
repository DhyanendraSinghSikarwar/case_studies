# syntax=docker/dockerfile:1
# Platform base image. Tag below is an EXAMPLE: check Docker Hub for current nvidia/cuda tags.
ARG CUDA_TAG=12.4.1-runtime-ubuntu22.04
FROM nvidia/cuda:${CUDA_TAG}
ENV DEBIAN_FRONTEND=noninteractive PIP_NO_CACHE_DIR=1
RUN apt-get update \
 && apt-get install -y --no-install-recommends python3 python3-pip \
 && rm -rf /var/lib/apt/lists/*
COPY constraints.txt /etc/ml-constraints.txt
ENV PIP_CONSTRAINT=/etc/ml-constraints.txt
LABEL org.example.base.version="2026.10"
