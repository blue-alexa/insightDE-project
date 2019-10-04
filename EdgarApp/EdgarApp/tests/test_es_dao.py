import unittest

from EdgarApp.es_dao import ES_ThirteenFHR_DAO, get_es_conn

def insert_test_es_records(conn):
    index_name = '13f-hr'
    type_name = 'form'
    conn.index()

def delete_test_es_records(conn):
    pass

class TestESDAO(unittest.TestCase):
    def setUp(self):
        es = ES_ThirteenFHR_DAO()
        es_conn = get_es_conn()

    def tearDown(self):
        delete_test_es_records(self.session)

    def test_get_by_date_range(self):
        pass