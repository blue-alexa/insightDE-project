import unittest

from EdgarApp.models import Index, getconn

def insert_test_records(session):
    sql = f"INSERT INTO filing_index(cik, company_name,  form_type, date_filed, accession_number, url) VALUES ("\
        f"'tcik1', 'tname1', 'tform1', '1998-01-10', 'taccess_no_1', '');"
    session.execute(sql)

def delete_test_records(session):
    pass

class TestModels(unittest.TestCase):
    def setUp(self):
        index = Index()
        self.session = getconn()
        insert_test_records(self.session)

    def tearDown(self):
        delete_test_records(self.session)

    def test_get_by_date_range(self):
        pass

