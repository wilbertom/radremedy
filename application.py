#!/usr/bin/env python
from remedy.radremedy import create_app
from remedy.rad import db
from remedy.bootstrap import strap
from remedy.get_save_data import run
from remedy.config import get_config_from_env
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

application = create_app(get_config_from_env())

manager = Manager(application)
Migrate(application, db, directory=application.config['MIGRATIONS_DIR'])
manager.add_command('db', MigrateCommand)


@manager.command
def bootstrap():
    strap(application)


@manager.command
def scrape():
    run(application)

if __name__ == '__main__':

    manager.run(default_command='runserver')

