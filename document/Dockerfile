FROM python:3.9.4

RUN mkdir /code \
&&apt-get update \
&&apt-get -y install freetds-dev \
&&apt-get -y install unixodbc-dev
COPY test_platform/ /code
COPY requirements.txt /code
COPY base.py /code
RUN pip install -r /code/requirements.txt -i https://pypi.douban.com/simple
WORKDIR /code
EXPOSE 8008

CMD ["python", "manage.py", "runserver", "0.0.0.0:8008"]