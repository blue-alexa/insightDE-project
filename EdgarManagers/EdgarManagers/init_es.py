import sys
sys.path.append("..")

from EdgarManagers.elasticsearch_dao.es_loader import ESLoader

loader = ESLoader()

index_name = "13f-hr"
type_name = "form"
mapping = {"form": {"properties": {
            "company_name": {"type": "text", "store": "true"},
            "report_date": {"type": "date", "store": "true"},
            "file_date": {"type": "date", "store": "true"},
            "cik": {"type": "keyword", "store": "true"},
            "holdings": {"type": "nested",
                         "properties": {
                             "nameOfIssuer": {"type": "text"},
                             "titleOfClass": {"type": "keyword"},
                             "cusip": {"type": "keyword"},
                             "value": {"type": "long"},
                             "shrsOrPrnAmt": {"type": "nested",
                                              "properties": {
                                                  "sshPrnamt": {"type": "long"},
                                                  "sshPrnamtType": {"type": "keyword"}
                                              }}
                         }}
        }}}

loader.create_mapping(index_name, type_name, mapping)