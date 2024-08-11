FROM python:3.9-slim

WORKDIR /AuthorizeAPI

RUN apt-get update && apt-get install -y \
    gcc \
    libc-dev \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY . /AuthorizeAPI

ENV FLASK_APP=auth.py

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["flask", "run"]
