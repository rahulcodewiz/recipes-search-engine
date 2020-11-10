# CourseProject

Please fork this repository and paste the github link of your fork on Microsoft CMT. Detailed instructions are on Coursera under Week 1: Course Project Overview/Week 9 Activities.

## Search engine guide

------
## Installation guide

### Go to search-engine-webapp directory


## Onetime setup-- Begin


### setup flaskr virtual environment & install it.

    python3 -m venv venv
    pip install -e .


### Download Elasticsearch/Kibana servers

    https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html
    https://www.elastic.co/guide/en/kibana/current/install.html

### Paste `elasticsearch.yml` from es-setup directory to `<ELASTICSEARCH-HOME>/conf`


### Start Elasticsearch and Kibana servers. Fix if there're any errors.


### Next step is launch the kibana UI and create index. This index will be used to store all documents and provide search features

- Kibana UI- localhost:5601
- Go to management-> Dev Tools
- Next copy the create index command from <project home>/es-setup/es-notes.txt and run from the dev tools


## Onetime setup-- End


### Activate virtual environment
    . venv/bin/activate


### Launch webapp
    export FLASK_APP=app
    export FLASK_ENV=development
    flask run

### Fix if there are any missing libraries

    python -m pip install json2html

## TODO: 
- set application port from config file
- Move to docker so same command works for everyone.
- Automate entire installation process 