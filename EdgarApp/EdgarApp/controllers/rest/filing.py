from datetime import datetime

from flask import abort, jsonify

from flask_restful import Resource, reqparse

from EdgarApp.es_dao import ES_ThirteenFHR_DAO

filing_parser = reqparse.RequestParser()
filing_parser.add_argument(
    'start',
    type=str,
    help='Start date of filing'
)

filing_parser.add_argument(
    'end',
    type=str,
    help='End date of filing'
)

filing_parser.add_argument(
    'cik',
    type=str,
    help='CIK of filing company'
)

filing_parser.add_argument(
    'cusip',
    type=str,
    help='CUSIP of 13F-HR holding'
)

class FilingAPI(Resource):
    def get(self):
        args = filing_parser.parse_args(strict=True)

        start = args['start']
        end = args['end']
        cik = args['cik']
        cusip = args['cusip']

        dao = ES_ThirteenFHR_DAO()
        if not start:
            start = '20190101'
        if not end:
            end = datetime.today().strftime("%Y%m%d")

        index_name = '13f-hr'
        result = {}

        if cik and not cusip:
            result = dao.filter_cik_with_date_range(index_name, start, end, cik)

        if cusip and not cik:
            result = dao.filter_cusip_with_date_range(index_name, start, end, cusip)

        if not cik and not cusip:
            result = dao.filter_date_range(index_name, start, end)

        if cik and cusip:
            result = dao.filter_cik_cusip_with_date_range(index_name, start, end, cik, cusip)

        if result:
            return jsonify(result)

        abort(400)

    # http://localhost:5000/filing_search?cusip=N14506104&start=20100101&end=20191001


