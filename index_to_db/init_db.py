"""
DB_USERNAME = 'edgar_user'
DB_PASSWORD = 'edgar_password'
DB_HOST = '52.37.185.37'
DB_PORT = '3306'
DB_NAME = 'edgar_db'

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()
rs = session.execute('SELECT * FROM test;')
for row in rs:
    print(row)
"""
import glob, os
from datetime import datetime


# source = '/data2/filing_index'
source = '../edgar_data_download/data/filings'
download_list_file = 'download_list.csv'

df = open(download_list_file, 'a')

for f in glob.glob(source + '/*.idx'):
    filename = os.path.basename(f)
    doc_date = filename.split('.')[1]
    print(f"Processing file {f}")
    with open(f, 'rb') as file:
        data = file.read()
        data = data.decode('ISO-8859-1')

        lines = data.split('\n')
        lines = lines[7:] # Skip first 7 lines of header

        for line in lines:
            data = line.strip().split("|")
            if len(data) == 5:
                for i, elem in enumerate(data):
                    data[i] = elem.strip()
                try:
                    data[3] = datetime.strptime(data[3], "%Y%m%d")
                except ValueError:
                    print(line)
                    data[3] = datetime.strptime(doc_date, "%Y%m%d")

                cik, company_name, form_type, date_filed, filing_content = data
                accession_no = filing_content.split("/")[-1].split(".")[0] # get accession number
                url = 'https://www.sec.gov/Archives/'+filing_content

                # write cik, company_name, form_type, date_filed, assession_no, url to database

                df.write(accession_no+'|'+url+'\n')

df.close()


