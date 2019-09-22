import glob, os
import logging
from logging.config import dictConfig
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc

logging_config = dict(
    version = 1,
    formatters = {
        'f': {'format':
              '%(asctime)s - %(name)s - %(levelname)s - %(message)s'}
        },
    handlers = {
        'fh': {'class': 'logging.FileHandler',
               'formatter': 'f',
               'level': logging.INFO,
               'filename': 'logger.log'},
        'ch': {'class': 'logging.StreamHandler',
               'formatter': 'f',
               'level': logging.INFO}
        },
    root = {
        'handlers': ['fh', 'ch'],
            'level': logging.INFO,
        }
)

dictConfig(logging_config)

# create logger
logger = logging.getLogger("index_to_db.init_db")

DB_USERNAME = 'edgar_user'
DB_PASSWORD = 'edgar_password'
DB_HOST = '34.219.152.31'
DB_PORT = '3306'
DB_NAME = 'edgar_db'

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

# source = '/data2/filing_index'
source = '../edgar_data_download/data/filings'

def clean(entry):
    entry = entry.strip()
    if "\\" in entry:
        entry = entry.replace("\\", "\\\\")
    if "'" in entry:
        entry = entry.replace("'", "''")
    return entry

for f in glob.glob(source + '/*.idx'):
    filename = os.path.basename(f)
    doc_date = filename.split('.')[1]
    print(f"Processing file {f}")
    with open(f, 'rb') as file:
        data = file.read()
        data = data.decode('ISO-8859-1')

        lines = data.split('\n')
        lines = lines[7:] # Skip first 7 lines of header
        cnt = 0
        for line in lines:
            data = line.strip().split("|")
            if len(data) == 5:
                for i, elem in enumerate(data):
                    data[i] = clean(elem)

                try:
                    data[3] = datetime.strptime(data[3], "%Y%m%d")
                except ValueError:
                    print(line)
                    data[3] = datetime.strptime(doc_date, "%Y%m%d")

                cik, company_name, form_type, date_filed, filing_content = data
                accession_no = filing_content.split("/")[-1].split(".")[0] # get accession number
                url = 'https://www.sec.gov/Archives/'+filing_content

                # write cik, company_name, form_type, date_filed, assession_no, url to database
                sql = f"INSERT INTO filing_index (cik, company_name, form_type, date_filed, accession_number, url) "\
                    f"VALUES('{cik}', '{company_name}', '{form_type}', '{date_filed.strftime('%Y-%m-%d')}', '{accession_no}', "\
                    f"'{url}');"

                try:
                    session.execute(sql)
                    session.commit()
                except exc.SQLAlchemyError:
                    logger.error(f"Failed to insert line: {line}")

                cnt += 1
    print(f"Processed {cnt} records in {f}")

session.close()


