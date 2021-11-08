FROM python:3.9.5-slim-buster

# set work directory
# WORKDIR /usr/src/app

# install dependencies
RUN pip install --upgrade pip
RUN apt-get update; apt-get install -y curl
RUN apt-get install -y libpq-dev postgresql postgresql-contrib gcc
#COPY ./requirements.txt /usr/src/app/requirements.txt
#RUN pip install -r requirements.txt

RUN pip install poetry

WORKDIR /code
COPY pyproject.toml /code/

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# Creating folders, and files for a project:
ENV PYTHONPATH "${PYTHONPATH}:/code:/code/brackend"
