import logging
from pytz import timezone

DB_USERNAME = 'edgar_user'
DB_PASSWORD = 'edgar_password'
DB_HOST = '10.0.0.11'
DB_PORT = '3306'
DB_NAME = 'edgar_db'

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

ELASTIC_HOST = '10.0.0.10'
ELASTIC_PORT = '9200'

ELASTIC_URI = f"{ELASTIC_HOST}:{ELASTIC_PORT}"

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
               'filename': 'es_feed_logger.log'},
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

local_timezone = timezone('US/Pacific')