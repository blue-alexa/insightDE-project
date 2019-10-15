import elasticsearch

from EdgarApp.config import DevConfig

def get_es_conn():
    conn = elasticsearch.Elasticsearch(DevConfig.ELASTIC_URI)
    return conn

class ES_ThirteenFHR_DAO(object):
    def __init__(self):
        self.conn = get_es_conn()
        self.size = 1000 # show first 1000 result

    def filter_date_range(self, index_name, start, end):
        """
        :param index_name:
        :param start:
        :param end:
        :return: {'found_records': xxx,
                  'result': [{'_index': xxx,
                              '_type': xxx,
                              '_id': xxx,
                              '_score': xxx,
                              '_source':{'company_name':xxx,
                                        'report_date': xxx,
                                        'file_date': xxx,
                                        'cik': xxx,
                                        'holdings': [
                                            {
                                            'nameOfIssuer':xxx,
                                            'titleOfClass': xxx,
                                            'cusip':xxx,
                                            'value': xxx,
                                            'shrsOrPrnAmt':
                                                {'sshPrnamt': xxx,
                                                'sshPrnamtType': xxx}
                                            },
                                            ...]
                                        }
                              },
                              ...]
                 }
        """
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

    def filter_id(self, id, index_name):
        """
        :param id: accession_number (_id)
        :param index_name: form type
        :return: {'result':{'company_name':xxx,
                            'report_date': xxx,
                            'file_date': xxx,
                            'cik': xxx,
                            'holdings': [
                                {
                                'nameOfIssuer':xxx,
                                'titleOfClass': xxx,
                                'cusip':xxx,
                                'value': xxx,
                                'shrsOrPrnAmt':
                                    {'sshPrnamt': xxx,
                                    'sshPrnamtType': xxx}
                                },
                                ...]
                            }
                    }
        """
        result = self.conn.search(index_name, {
            "query": {
                "term": {
                    "_id": f'{id}'
                }
            }
        })
        print(result)
        return {'result': result['hits']['hits'][0]['_source']}


es_dao = ES_ThirteenFHR_DAO()