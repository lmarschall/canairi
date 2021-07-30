FROM python:3.7

# copy software folders
COPY ./ /server
COPY /requirements.txt /server/requirements.txt

# install python requirements
RUN pip install -r /server/requirements.txt

CMD ["python", "manage.py" "runserver", "0.0.0.0:8000"]