FROM python:3.9-alpine3.16

# WORKDIR нужна, чтобы если мы посылали команды в контейтер, то они бы выполнялись из этой папки
WORKDIR /service
EXPOSE 8000

COPY requirements.txt /temp/requirements.txt
#RUN - это сразу запустить команду
RUN apk add postgres-client build-base posgresql-dev
RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password service-user
COPY service /service

# USER - выбор основного юзера для запуска команд, например.
USER service-user