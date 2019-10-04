import logging

s3_filing_path = 'data/filings'
s3_log_path = 'data/log_file'
bucket_name = 'miniminds-edgar-data'

DB_USERNAME = 'edgar_user'
DB_PASSWORD = 'edgar_password'
DB_HOST = '10.0.0.11'
DB_PORT = '3306'
DB_NAME = 'edgar_db'

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

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

RABBITMQ_USER = 'rabbitmq'
RABBITMQ_PASS = 'rabbitmq'
RABBITMQ_HOST = '10.0.0.14'

CELERY_BROKER_URL = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}//"