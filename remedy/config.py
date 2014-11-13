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
    DEBUG = False
    SECRET_KEY = os.environ.get('RAD_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'mysql://{0}:{1}@{2}/{3}'.format(os.environ.get('RDS_USERNAME'),
                                                               os.environ.get('RDS_PASSWORD'),
                                                               os.environ.get('RDS_HOSTNAME'),
                                                               os.environ.get('RDS_DB_NAME'))


CONFIGURATIONS = {
    'production': ProductionConfig,
    'testing': DevelopmentConfig,
    'development': DevelopmentConfig,
}

def get_config_by(name=None):
    """
    Get the correct configuration class based on the name passed.
    Name should be one of:

    1. production
    2. testing
    3. development

    We default to "development"
    """

    if name is None:
        name = 'development'

    return CONFIGURATIONS[name]


def get_config_from_env(default=None):
    """
    Get the right configuration class name on runtime from the environment.
    This function looks for a variable called `RAD_CONFIG`. The value of this
    variable should be one from `get_config_by`.

    This function doesn't force that variable to be in the environment.

    """
    return os.environ.get('RAD_CONFIG', default)
