FROM python:3.11-slim-buster
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git curl


COPY requirements.txt requirements.txt
COPY schema.prisma schema.prisma

RUN pip3 install -r requirements.txt
RUN prisma generate

COPY ./src src

WORKDIR /src

CMD [ "gunicorn","-k","uvicorn.workers.UvicornWorker","--bind","0.0.0.0:8081","app:app"]
