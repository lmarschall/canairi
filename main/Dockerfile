FROM python:3.7

# copy software folders
COPY ./ /main
COPY /requirements.txt /main/requirements.txt

# install python requirements
RUN pip install -r /main/requirements.txt

CMD ["python", "-m", "main"]