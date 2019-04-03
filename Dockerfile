FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD dns /code/dns
ADD funcs.py /code/
ADD server.py /code/
ADD dnssec/ /code/dnssec
ADD config.py /code/
ADD psql/ /code/psql
ADD ram_orm/ /code/ram_orm
