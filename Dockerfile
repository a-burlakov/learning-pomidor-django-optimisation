FROM python:3.9-alpine3.16

COPY requirements.txt /temp/requirements.txt
COPY service /service
# WORKDIR нужна, чтобы если мы посылали команды в контейтер, то они бы выполнялись из этой папки
WORKDIR /service
EXPOSE 8000

#RUN - это сразу запустить команду
RUN pip install - r /temp/requirements.txt

RUN adduser --disabled-password service-user

# USER - выбор основного юзера для запуска команд, например.
USER service-user