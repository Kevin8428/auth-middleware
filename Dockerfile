FROM ubuntu:18.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update -qq \
    && apt-get install -y wget python3-pip vim curl
RUN apt update
RUN apt install postgresql postgresql-contrib python-psycopg2 libpq-dev sudo -f -y
RUN pip3 install pyjwt ipython Flask psycopg2

ENV PSQL_DIR=/usr/bin/psql
ENV PATH="$PSQL_DIR:$PATH"
ENV DBNAME=authdb_dev
ENV HOST=localhost
ENV DBUSER=postgres
ENV DBPASSWORD=password
ENV AUTHSECRET=secret
ENV FLASK_APP=auth.py
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
WORKDIR /app
COPY . /app