#
# import elasticsearch
#
# es = elasticsearch.Elasticsearch()
#
# es = elasticsearch.Elasticsearch(["10.0.0.10:9200"])
#
# index_name = "13f-hr"
# type_name = "form"
#
# if es.indices.exists(index_name):
#     es.indices.delete(index_name)
#
# es.indices.create(index_name)
# es.cluster.health(wait_for_status="yellow")
#
# es.indices.put_mapping(index=index_name, doc_type=type_name, body={"form":{"properties":{
#     "company_name": {"type": "text", "store": "true"},
#     "report_date": {"type": "date", "store": "true"},
#     "file_date": {"type": "date", "store": "true"},
#     "cik": {"type": "keyword", "store": "true"},
#     "holdings": {"type": "nested",
#                  "properties": {
#                      "nameOfIssuer": {"type": "text"},
#                      "titleOfClass": {"type": "keyword"},
#                      "cusip": {"type": "keyword"},
#                      "value": {"type": "long"},
#                      "shrsOrPrnAmt": {"type": "nested",
#                                       "properties": {
#                                           "sshPrnamt": {"type": "long"},
#                                           "sshPrnamtType": {"type": "keyword"}
#                                       }}
#                  }}
# }}})
#
#
#
# import os, json
# target_folder = '../edgar_data_download/data/thirteenF_json'
# test = '0001172661-19-000001.txt'
# with open(os.path.join(target_folder, test), 'r') as f:
#     data = json.load(f)
#
# data = {'company_name': 'Brenner West Capital Advisors, LP', 'report_date': '20181231', 'file_date': '20190102', 'cik': '0001425999', 'holdings': [{'nameOfIssuer': 'N/A', 'titleOfClass': 'N/A', 'cusip': '000000000', 'value': '0', 'shrsOrPrnAmt': {'sshPrnamt': '0', 'sshPrnamtType': 'SH'}}]}
#
# es.index(index=index_name, doc_type=type_name, id=1, body=data)
#
# print(data)
#
# from pprint import pprint
# res = es.search(index=index_name, body={"query": {"match_all": {}}})
# pprint(res)


import logging
import elasticsearch

from config import ELASTIC_URI

class ESLoader(object):
    def __init__(self):
        self.conn = elasticsearch.Elasticsearch([ELASTIC_URI])
        self.logger = logging.getLogger("es_feed.es_loader")

    def create_mapping(self, index_name, type_name, mapping):
        # remove index if exist
        if self.conn.indices.exists(index_name):
            self.conn.indices.delete(index_name)
        self.conn.indices.put_mapping(index=index_name, doc_type=type_name, body=mapping)
        self.logger.info(f"Mapping created {mapping}")

    def insert(self, index_name, type_name, id, body):
        self.conn.index(index=index_name, doc_type=type_name, id=id, body=body)
        self.logger.info(f"Inserted {id} to ElasticSearch")

