FROM python:3.10

# os setup
RUN apt-get update && apt-get -y install \
  python3-lxml \
  build-essential \
  libssl-dev \
  libffi-dev \
  python3-dev \
  libxml2-dev \
  libxslt1-dev \
  && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# install requirements
COPY utils /usr/src/utils
COPY crawler/requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
RUN rm -rf /usr/src/utils

# move codebase over
COPY crawler /usr/src/app

# copy testing script into container
COPY docker/run_docker_tests.sh /usr/src/app/run_docker_tests.sh

# run the spider
CMD ["scrapy", "crawl", "link"]