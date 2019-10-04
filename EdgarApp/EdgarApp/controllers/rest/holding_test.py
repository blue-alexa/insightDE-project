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
    }, size=1000)

len(res['hits']['hits'])

import requests
url = 'http://10.0.0.10:9200/13f-hr/_search?pretty=true&q=holdings.cusip:177376100'
# url = 'http://10.0.0.10:9200/13f-hr/_search?pretty=true&q=file_date:20190620'


# date range query
res = es.search(index_name, {
    "query": {
        "range": {
            "file_date": {
                "gte": "20190101",
                "lte": "20190103"
            }
        }
    }
}, size=1000)
res['hits']['hits'][0]['_source']['file_date']
"""
curl -XPOST -H "Content-Type: application/json" 'http://10.0.0.10:9200/13f-hr/form/_search?pretty=true' -d '{
    "query": {
        "range" : {
            "file_date" : {
                "gte": "20190101",
                "lte": "20190110"
            }
        }
    }
}
'
"""

res = es.search(index_name, {
        "query": {
            "bool": {
                "must": [
                    {
                        "range" : {
                            "file_date" : {
                                "gte": "2019-07-01",
                                "lte": "2019-10-10"
                            }
                        }
                    },
                    {
                        "nested": {
                            "path": "holdings",
                            "query": {
                                "bool": {
                                    "must": {
                                        "match": {"holdings.cusip": "N14506104"}
                                    }
                                }
                            }
                        }
                    }
                ]
            }
        }
}, size=1000)
start = "20190101"
end = "20190110"

result = es.search(index_name, {
    "query": {
        "range": {
            "file_date": {
                "gte": f'{start}',
                "lte": f'{end}'
            }
        }
    }
}, size=1000)

res = es.search(index_name, {
        "query": {
            "bool": {
                "must": [
                    {
                        "range" : {
                            "file_date" : {
                                "gte": "20190701",
                                "lte": "20191010"
                            }
                        }
                    },
                    {
                        "term": {
                            "cik":'0001531971'
                        }
                    }
                ]
            }
        }
}, size=1000)



