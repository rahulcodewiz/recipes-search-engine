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

USER_IDX = 1

@app.route('/')
def home():
   return render_template('index.html')

#TODO(Jon) test recommend call 
@app.route('/search' , methods=['POST'])
def recommend():
   return searchEs(recommenderSystem(USER_IDX))

@app.route('/search' , methods=['POST'])
def search():
   return searchEs(request.form['recipesText'])

@app.route('/autosuggest' , methods=['POST'])
def autosuggest():
   reqData = str(request.data,'utf-8')
   return autosuggestPhrase(reqData)

if __name__ == '__main__':
   app.run()

