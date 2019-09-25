from flask import Flask

from edgar_UI.models import Index
from edgar_UI.extensions import rest_api

from edgar_UI.controllers.rest.f_index import IndexAPI

def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    rest_api.add_resource(IndexAPI, '/index')
    rest_api.init_app(app)


    return app

if __name__ == "__main__":
    app.run(debug=True)

