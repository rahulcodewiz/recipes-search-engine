#!/bin/bash
echo "Starting Elastic Server"
cd /app/elasticsearch-7.10.0/
cmd="./bin/elasticsearch"

export FLASK_APP=app
export FLASK_ENV=development
$cmd > /dev/null 2>&1 &
flask run -h 0.0.0.0 -p 5000