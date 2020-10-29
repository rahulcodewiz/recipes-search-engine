from flask import Flask
import os
def create_app(app_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile("config.py", silent=True)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello():
        return "Hello, World!"
    return app