FROM python:3.10.13-alpine3.18 as builder

RUN apk add --no-cache \
    wget \
    tar \
    firefox

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz \
    && tar -xvzf geckodriver* \
    && chmod +x geckodriver \
    && mv geckodriver /usr/local/bin/


# Create a new user and switch to it
RUN adduser -D -h /home/scraper scraper

USER scraper

WORKDIR /home/scraper

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

USER root

RUN chown -R scraper:scraper /home/scraper
RUN chmod -R 755 /home/scraper

USER scraper