FROM ubuntu:20.04

# OS update, then clean up
RUN apt-get -yq update && \
    apt-get -yq upgrade && \
    apt-get -yq --no-install-recommends install \
        software-properties-common \
        apt-transport-https \
        ca-certificates \
        aptitude \
        wget \
        unzip && \
    apt-get clean && \
    rm -rf /tmp/* /var/tmp/* /var/lib/apt/archive/* /var/lib/apt/lists/*

# copy software folders
COPY /client /client
COPY /main /main
COPY /server /server

# install python requirements
COPY /requirements.txt /main/requirements.txt
RUN pip install -r /main/requirements.txt