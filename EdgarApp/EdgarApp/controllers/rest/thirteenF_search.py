from datetime import datetime

from flask import abort, jsonify

from flask_restful import Resource, reqparse

from EdgarApp.es_dao import ES_ThirteenFHR_DAO

thirteenF_parser = reqparse.RequestParser()


thirteenF_parser.add_argument(
    'cik',
    type=str,
    help='CIK of filing company'
)

thirteenF_parser.add_argument(
    'cusip',
    type=str,
    help='CUSIP of 13F-HR holding'
)

thirteenF_parser.add_argument(
    'period1',
    type=str,
    help='Start date of filing, format YYYYMMDD'
)

thirteenF_parser.add_argument(
    'period2',
    type=str,
    help='End date of filing, format YYYYMMDD'
)

class ThirteenFAPI(Resource):
    def get(self):
        args = thirteenF_parser.parse_args(strict=True)

        start = args['period1']
        end = args['period2']
        cik = args['cik']
        cusip = args['cusip']

        dao = ES_ThirteenFHR_DAO()
        if not start:
            start = '2019-01-01'
        else:
            start = start[:4] + "-" + start[4:6] + "-" + start[6:] #change date format to YYYY-MM-DD

        if not end:
            end = datetime.today().strftime("%Y-%m-%d")
        else:
            end = end[:4] + "-" + end[4:6] + "-" + end[6:]

        print(f"start: {start}, end: {end}, cik: {cik}, cusip: {cusip}")

        index_name = '13f-hr'
        data = {}

        if cik and not cusip:
            data = dao.filter_cik_with_date_range(index_name, start, end, cik)

        if cusip and not cik:
            data = dao.filter_cusip_with_date_range(index_name, start, end, cusip)

        if not cik and not cusip:
            data = dao.filter_date_range(index_name, start, end)

        if cik and cusip:
            data = dao.filter_cik_cusip_with_date_range(index_name, start, end, cik, cusip)

        if data:
            res = []
            for i, hit in enumerate(data['result']):
                res.append({
                            'accession_number': hit['_id'],
                            'cik': hit['_source']['cik'],
                            'company_name': hit['_source']['company_name'],
                            'file_date': hit['_source']['file_date'],
                            'report_date': hit['_source']['report_date']
                            })

            return jsonify({'result': res})

        abort(400)






