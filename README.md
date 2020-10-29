# CourseProject

Please fork this repository and paste the github link of your fork on Microsoft CMT. Detailed instructions are on Coursera under Week 1: Course Project Overview/Week 9 Activities.

## Search engine guide

### Go to search-engine-webapp directory

### Setup flaskr virtual environment & install it. It's one time activity

    python3 -m venv venv
    pip install -e .


### Activate virtual environment
    . venv/bin/activate

### Launch webapp
    export FLASK_APP=search-engine
    export FLASK_ENV=development
    flask run

## TODO: 
- set application port from config file
- Move to docker so same command works for everyone.
- Automate entire installation process 