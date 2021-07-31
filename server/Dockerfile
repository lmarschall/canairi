FROM python:3.7

# set work directory
WORKDIR /usr/src/server

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy software folders
COPY . .
COPY ./requirements.txt .

# install python requirements
RUN pip install -r requirements.txt