#!/bin/bash

#TODO: FIX This-
# ES path should be system specific. 
#Better way to handler this is ask user to set ES_HOME. Check if ES_HOME env variable is not present then throw error
# Start Elasticsearch only if server is not running.
echo "Starting Elastic Server"
cd /app/elasticsearch-7.10.0/
cmd="./bin/elasticsearch"

export FLASK_APP=app
export FLASK_ENV=development
$cmd > /dev/null 2>&1 &
flask run
