FROM python:3.9.17-slim-bullseye
RUN apt-get update --allow-releaseinfo-change && \
    apt-get install -y \
    build-essential \
    bc \
    cmake \
    git \
    gzip \
    libgsl-dev \
    vim \
    wget    
ENV HTTP_PROXY=http://10.243.1.2:8080 HTTPS_PROXY=http://10.243.1.2:8080
RUN pip3 install \
    biopython \
    flask \
    jinja2 \
    openpyxl \
    pandas
WORKDIR /work
CMD ["/bin/bash"]