#!/bin/bash

# Start Spark master
$SPARK_HOME/sbin/start-master.sh

# Start Spark worker
$SPARK_HOME/sbin/start-worker.sh spark://spark:7077

# tail -f /dev/null
echo "Asked to decommission"
# Find the pid to signal
tail -f $SPARK_HOME/logs/*