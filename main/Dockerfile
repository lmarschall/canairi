FROM python:3.7-slim

# set work directory
WORKDIR /usr/src/main

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy software folders
COPY . .
COPY ./requirements.txt .

# install build packages
RUN apt-get update
RUN apt-get -y install make gcc

# install python requirements
RUN pip install -r requirements.txt