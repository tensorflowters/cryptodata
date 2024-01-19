FROM python:3.10.13

RUN mkdir /home/consumer

WORKDIR /home/consumer

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
