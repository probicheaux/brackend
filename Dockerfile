FROM python:3.9.5-slim-buster

# set work directory
# WORKDIR /usr/src/app

# install dependencies
RUN pip install --upgrade pip
RUN apt-get update; apt-get install -y curl
#COPY ./requirements.txt /usr/src/app/requirements.txt
#RUN pip install -r requirements.txt

RUN pip install poetry

WORKDIR /code
COPY poetry.lock pyproject.toml /code/

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY . /code
ENV PYTHONPATH "${PYTHONPATH}:/code:/code/brackend"
