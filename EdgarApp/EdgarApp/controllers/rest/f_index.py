from datetime import datetime

from flask import abort, jsonify

from flask_restful import Resource, reqparse

from EdgarApp.models import getconn

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
        args = index_parser.parse_args(strict=True)

        cik = args['cik']
        form_type = args['form_type']
        start = args['period1']
        end = args['period2']

        if start:
            start_date = datetime.strptime(start, "%Y%m%d").strftime("%Y-%m-%d")
        else:
            start_date = '2000-01-01'

        if end:
            end_date = datetime.strptime(end, "%Y%m%d").strftime("%Y-%m-%d")
        else:
            end_date = datetime.today().strftime("%Y-%m-%d")

        session = getconn()
        rs = None

        if not cik and not form_type:
            sql = f"SELECT * FROM filing_index WHERE date_filed >= '{start_date}' AND date_filed <= '{end_date}';"
            rs = session.execute(sql).fetchall()

        if cik and not form_type:
            sql = f"SELECT * FROM filing_index WHERE cik='{cik}'AND date_filed >= '{start_date}' AND date_filed <= '{end_date}';"
            rs = session.execute(sql).fetchall()

        if not cik and form_type:
            sql = f"SELECT * FROM filing_index WHERE form_type='{form_type}'AND date_filed >= '{start_date}' AND date_filed <= '{end_date}';"
            rs = session.execute(sql).fetchall()

        if cik and form_type:
            sql = f"SELECT * FROM filing_index WHERE cik='{cik}'AND form_type='{form_type}'AND date_filed >= '{start_date}' AND date_filed <= '{end_date}';"
            rs = session.execute(sql).fetchall()

        if rs:
            data = [dict(row) for row in rs]
            return jsonify({'result': data})


        abort(400)


    # http://localhost:5000/filing_index?cik=320193&form_type=10-Q
    # http://localhost:5000/filing_index?cik=320193&form_type=10-Q&period2=20100101
    # curl localhost:5000/index?cik=320193&form_type=10-Q&period2=20100101


