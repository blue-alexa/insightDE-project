class Config(object):
    SECRET_KEY = 'SECRETKEYFOREDGARPROJECT'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(Config):
    DB_USERNAME = 'edgar_user'
    DB_PASSWORD = 'edgar_password'
    DB_HOST = '34.219.152.31'
    DB_PORT = '3306'
    DB_NAME = 'edgar_db'

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    DEBUG = True