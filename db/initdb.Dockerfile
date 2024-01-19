FROM python:3.10.13

RUN mkdir /home/initdb

WORKDIR /home/initdb

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
