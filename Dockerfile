FROM python:2

RUN apt-get update

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install pre-commit
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get -y install rubygems

COPY . .
