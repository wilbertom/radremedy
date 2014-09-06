"""
config.py

Looks for the RAD_PRODUCTION variable and creates path to database 
"""
import os

_basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'rad/rad.db')
    MIGRATIONS_DIR = './remedy/rad/migrations'
    SECRET_KEY = 'Our little secret'


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    Debug = False
    SQLALCHEMY_DATABASE_URI = 'mysql://{0}:{1}@{2}/{3}'.format(os.environ.get('RDS_USERNAME'),
                                                               os.environ.get('RDS_PASSWORD'),
                                                               os.environ.get('RDS_HOSTNAME'),
                                                               os.environ.get('RDS_DB_NAME'))
