from flask import Flask

from EdgarApp.models import Index
from EdgarApp.extensions import rest_api

from EdgarApp.controllers.rest.f_index import IndexAPI
from EdgarApp.controllers.rest.filing import FilingAPI

from EdgarApp.controllers.main import main_blueprint


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    rest_api.add_resource(IndexAPI, '/filing_index')
    rest_api.add_resource(FilingAPI, '/filing_search')
    rest_api.init_app(app)

    app.register_blueprint(main_blueprint)

    return app

if __name__ == "__main__":
    app.run(debug=True)

