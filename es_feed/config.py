import logging

DB_USERNAME = 'edgar_user'
DB_PASSWORD = 'edgar_password'
DB_HOST = '52.35.91.126'
DB_PORT = '3306'
DB_NAME = 'edgar_db'

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

ELASTIC_IP = '10.0.0.10'
ELASTIC_HOST = '9200'

ELASTIC_URI = f"{ELASTIC_IP}:{ELASTIC_HOST}"

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