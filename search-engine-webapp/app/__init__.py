from flask import Flask, redirect, url_for, render_template, request, flash
import os
from flask import Flask, render_template
from json2html import *
import requests
import json
import os
from .search_service import *
app = Flask(__name__)
app.config.from_pyfile('setup.cfg', silent=True)

@app.route('/')
def home():
   return render_template('index.html')


@app.route('/search' , methods=['POST'])
def search():
   return searchEs(request.form['recipesText'])

@app.route('/autosuggest' , methods=['POST'])
def autosuggest():
   reqData = request.data
   return autosuggestES(reqData)

if __name__ == '__main__':
   app.run()

