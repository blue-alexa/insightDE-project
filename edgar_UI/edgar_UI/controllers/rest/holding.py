# test elasticsearch results
import elasticsearch
from pprint import pprint
es = elasticsearch.Elasticsearch(['10.0.0.10:9200'])
index_name = '13f-hr'
type_name = 'form'

es.cluster.health(wait_for_status="yellow")
res = es.search(index_name, {
        "query": {
            "query_string": {
                "query": "holdings.nameOfIssuer:VISA*"
            }
        }
    })

pprint(res)

res = es.search(index_name, {
        "query": {
            "query_string": {
                "query": "file_date:20190620"
            }
        }
    })

pprint(res)

res = es.search(index_name, {
        "query": {
            "nested": {
                "path": "holdings",
                "query": {
                    "bool":{
                        "must": {
                            "match": {"holdings.cusip":"177376100"}
                        }
                    }
                }
            }
        }
    })
len(res['hits']['hits'])
pprint(res['hits']['hits'])

res = es.search(index_name, {
        "query": {
            "nested": {
                "path": "holdings",
                "query": {
                    "bool":{
                        "must": {
                            "match": {"holdings.cusip":"N14506104"}
                        }
                    }
                }
            }
        }
    })
len(res['hits']['hits'])

import requests
url = 'http://10.0.0.10:9200/13f-hr/_search?pretty=true&q=holdings.cusip:177376100'
# url = 'http://10.0.0.10:9200/13f-hr/_search?pretty=true&q=file_date:20190620'


session = requests.Session()
response = session.get(url)