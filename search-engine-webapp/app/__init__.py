from flask import Flask, redirect, url_for, render_template, request, flash
import os
from flask import Flask, render_template
from json2html import *
import requests
import json
import os
from elasticsearch import Elasticsearch

app = Flask(__name__)
app.config.from_pyfile('setup.cfg', silent=True)

es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])
@app.route('/')
def home():
   return render_template('index.html')


@app.route('/search' , methods=['POST'])
def search():
   return searchEs(request.form['recipesText'])


if __name__ == '__main__':
   app.run()


def searchEs(term):
   query = json.dumps({
        "query": {
            "match": {
                "title": term
            }
        }
    })
   res = es.search(index="recipes_idx1", body=query)
   return json2html.convert(json = res)
