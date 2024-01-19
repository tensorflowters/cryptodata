ARG ALPINE_VERSION=3.18
ARG PYTHON_VERSION=3.11.6

FROM python:${PYTHON_VERSION}-alpine${ALPINE_VERSION}

ARG HADOOP_VERSION=3
ARG JAVA_VERSION=17
ARG SPARK_VERSION=3.5.0
ARG SPARK_DOWNLOAD_URL=https://dlcdn.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

RUN apk update && \
    apk add --no-cache \
    bash \
    ca-certificates \
    coreutils \
    openjdk${JAVA_VERSION}-jre-headless \
    openssl \
    procps \
    wget && \
    rm /bin/sh && \
    ln -sv /bin/bash /bin/sh && \
    wget -O spark.gz ${SPARK_DOWNLOAD_URL} && \
    tar -xvf spark.gz -C /home && \
    mv /home/spark-3.5.0-bin-hadoop3 /home/spark && \
    rm -rf spark.gz && \
    addgroup spark && \
    adduser \
    --disabled-password \
    --gecos 'Spark User' \
    --home /home/spark \
    --ingroup spark \
    --shell /bin/bash \
    spark spark && \
    chown -R spark:spark /home/spark && \
    chmod -R 775 /home/spark

WORKDIR /home/spark

COPY spark-entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV SPARK_HOME=/home/spark
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin

USER spark

ENTRYPOINT [ "/entrypoint.sh" ]