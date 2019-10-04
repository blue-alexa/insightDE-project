SEC_QUERY_START_DATE = '2000-01-01'

class Config(object):
    SECRET_KEY = 'SECRETKEYFOREDGARPROJECT'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(Config):
    DB_USERNAME = 'edgar_user'
    DB_PASSWORD = 'edgar_password'
    DB_HOST = '10.0.0.11'
    DB_PORT = '3306'
    DB_NAME = 'edgar_db'

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    ELASTIC_HOST = '10.0.0.10'
    ELASTIC_PORT = '9200'

    ELASTIC_URI = [f"{ELASTIC_HOST}:{ELASTIC_PORT}"]

    DEBUG = True

