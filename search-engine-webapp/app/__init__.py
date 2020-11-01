from flask import Flask, redirect, url_for, render_template, request, flash
import os
from flask import Flask, render_template
app = Flask(__name__)
app.config.from_pyfile('setup.cfg', silent=True)
@app.route('/')
def home():
   return render_template('index.html')
if __name__ == '__main__':
   app.run()