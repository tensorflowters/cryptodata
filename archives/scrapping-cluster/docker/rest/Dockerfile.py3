FROM python:3.10

# os setup
RUN apt-get update
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# install requirements
COPY utils /usr/src/utils
COPY rest/requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
RUN rm -rf /usr/src/utils

# move codebase over
COPY rest /usr/src/app

# copy testing script into container
COPY docker/run_docker_tests.sh /usr/src/app/run_docker_tests.sh

# run command
CMD ["python", "rest_service.py"]