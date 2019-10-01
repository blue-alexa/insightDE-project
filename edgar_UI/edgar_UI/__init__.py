from flask import Flask

from edgar_UI.models import Index
from edgar_UI.extensions import rest_api

from edgar_UI.controllers.rest.f_index import IndexAPI

from edgar_UI.controllers.main import main_blueprint


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    rest_api.add_resource(IndexAPI, '/filings')
    rest_api.init_app(app)

    app.register_blueprint(main_blueprint)

    return app

if __name__ == "__main__":
    app.run(debug=True)

