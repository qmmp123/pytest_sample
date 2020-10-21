FROM python:3.8

ENV pythonunbuffered 1

COPY reqs.pip /code/reqs.pip
RUN pip install -r /code/reqs.pip

WORKDIR /code/
