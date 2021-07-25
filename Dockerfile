FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 0

# Sane defaults for pip
ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

COPY requirements.txt /tmp/requirements/

RUN pip install -r /tmp/requirements/requirements.txt

COPY . .

# add our user and group first to make sure their IDs get assigned consistently
RUN groupadd -r deployer && useradd -r -m -g deployer deployer && chown -R deployer:deployer /app

EXPOSE 8000

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
