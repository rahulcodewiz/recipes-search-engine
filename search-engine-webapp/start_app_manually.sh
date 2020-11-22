#!/bin/bash
echo "Check if ElasticSearch is running"
es_status=`curl 'localhost:9200'`
if [[ "$es_status" == *"not"* ]]; then
    echo "Starting Elastic Server"
    export ES_HOME="${ES_HOME:-'/app/elasticsearch-7.10.0/'}"
    echo "Starting Elastic Search from ${ES_HOME}"
    bash ${ES_HOME}/bin/elasticsearch > /dev/null 2>&1 &
    if [ $? -ne 0 ]; then
    echo "Failed to start ElasticSearch"
    exit 1
    fi
else
    echo "Elastic Search is running: $es_status"
fi

export FLASK_APP="${FLASK_APP:-app}"
export FLASK_ENV="${FLASK_APP:-development}"
flask run -h 0.0.0.0 -p 5000