import elasticsearch

from edgar_UI.config import DevConfig

def get_es_conn():
    conn = elasticsearch.Elasticsearch(DevConfig.ELASTIC_URI)
    return conn

class ES_ThirteenFHR_DAO(object):
    def __init__(self):
        self.conn = get_es_conn()
        self.size = 1000 # show first 1000 result

    def filter_date_range(self, index_name, start, end):
        result = self.conn.search(index_name, {
            "query": {
                "range": {
                    "file_date": {
                        "gte": f'{start}',
                        "lte": f'{end}'
                    }
                }
            }
        }, size = self.size)

        return {'found_records': result['hits']['total'],
                'result': result['hits']['hits']}

    def filter_cusip_with_date_range(self, index_name, start, end, cusip):
        result = self.conn.search(index_name, {
            "query": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                "file_date": {
                                    "gte": f'{start}',
                                    "lte": f'{end}'
                                }
                            }
                        },
                        {
                            "nested": {
                                "path": "holdings",
                                "query": {
                                    "bool": {
                                        "must": {
                                            "match": {"holdings.cusip": f'{cusip}'}
                                        }
                                    }
                                }
                            }
                        }
                    ]
                }
            }
        }, size=self.size)

        return {'found_records': result['hits']['total'],
                'result': result['hits']['hits']}

    def filter_cik_with_date_range(self, index_name, start, end, cik):
        result = self.conn.search(index_name, {
            "query": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                "file_date": {
                                    "gte": f'{start}',
                                    "lte": f'{end}'
                                }
                            }
                        },
                        {
                            "term": {
                                "cik": f'{cik}'
                            }
                        }
                    ]
                }
            }
        }, size=self.size)

        return {'found_records': result['hits']['total'],
                'result': result['hits']['hits']}

    def filter_cik_cusip_with_date_range(self, index_name, start, end, cik, cusip):
        result = self.conn.search(index_name, {
            "query": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                "file_date": {
                                    "gte": f'{start}',
                                    "lte": f'{end}'
                                }
                            }
                        },
                        {
                            "nested": {
                                "path": "holdings",
                                "query": {
                                    "bool": {
                                        "must": {
                                            "match": {"holdings.cusip": f'{cusip}'}
                                        }
                                    }
                                }
                            }
                        },
                        {
                            "term": {
                                "cik": f'{cik}'
                            }
                        }
                    ]
                }
            }
        }, size=self.size)

        return {'found_records': result['hits']['total'],
                'result': result['hits']['hits']}

