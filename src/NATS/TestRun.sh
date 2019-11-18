#!/bin/sh

export NATS_HOME=${PWD}

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$NATS_HOME/dist:/usr/lib64

java -cp dist/nats-standalone.jar:dist/nats-client.jar:dist/nats-shared.jar:dist/json.jar:dist/commons-logging-1.2.jar -Xmx768m TestRun $1
