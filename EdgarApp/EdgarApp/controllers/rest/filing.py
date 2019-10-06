from flask import jsonify

from flask_restful import Resource, reqparse

from EdgarApp.es_dao import ES_ThirteenFHR_DAO

filing_parser = reqparse.RequestParser()


filing_parser.add_argument(
    '_id',
    type=str,
    help='Accession number'
)

class FilingAPI(Resource):
    def get(self):
        args = filing_parser.parse_args(strict=True)

        id = args['_id']
        index_name = '13f-hr'

        dao = ES_ThirteenFHR_DAO()
        res = dao.filter_id(id, index_name)
        return jsonify(res)

    # http://35.160.70.126:5000/filing?_id=0001531971-19-000004
