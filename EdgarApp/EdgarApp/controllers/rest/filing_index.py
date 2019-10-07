from datetime import datetime

from flask import abort, jsonify

from flask_restful import Resource, reqparse

from EdgarApp.models import Index
from EdgarApp.config import SEC_QUERY_START_DATE

index_parser = reqparse.RequestParser()
index_parser.add_argument(
    'cik',
    type=str,
    help='Central Index Key'
)

index_parser.add_argument(
    'form_type',
    type=str,
    help='Form type'
)

index_parser.add_argument(
    'period1',
    type=str,
    help='Start date, format YYYYMMDD'
)

index_parser.add_argument(
    'period2',
    type=str,
    help='End date, format YYYYMMDD'
)


class IndexAPI(Resource):
    def get(self):
        args = index_parser.parse_args()

        cik = args['cik']
        form_type = args['form_type']
        start = args['period1']
        end = args['period2']

        if start:
            start_date = datetime.strptime(start, "%Y%m%d").strftime("%Y-%m-%d")
        else:
            start_date = SEC_QUERY_START_DATE

        if end:
            end_date = datetime.strptime(end, "%Y%m%d").strftime("%Y-%m-%d")
        else:
            end_date = datetime.today().strftime("%Y-%m-%d")

        index = Index()
        data = {}

        if not cik and not form_type:
            data = index.get_by_date_range(start_date, end_date)

        if cik and not form_type:
            data = index.get_by_cik_and_date_range(cik, start_date, end_date)

        if not cik and form_type:
            data = index.get_by_form_type_and_date_range(form_type, start_date, end_date)

        if cik and form_type:
            data = index.get_by_cik_form_type_date_range(cik, form_type, start_date, end_date)

        if data:
            return jsonify({'result': data})

        abort(400)

