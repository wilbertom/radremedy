"""
radremedy.py

Main web application file. Contains initial setup of database, API, and other components.
Also contains the setup of the routes.
"""
from flask import Flask
from flask.ext.login import current_user
from remedy.config import get_config_by
from remedy.rad import db


def create_app(config_name=None):

    app = Flask(__name__)
    app.config.from_object(get_config_by(config_name))

    from remedyblueprint import remedy, url_for_other_page
    app.register_blueprint(remedy)

    from admin import admin
    admin.init_app(app)

    from auth.user_auth import auth, login_manager
    app.register_blueprint(auth)
    login_manager.init_app(app)

    # searching configurations
    app.jinja_env.trim_blocks = True
    # Register the paging helper method with Jinja2
    app.jinja_env.globals['url_for_other_page'] = url_for_other_page
    app.jinja_env.globals['logged_in'] = lambda : not current_user.is_anonymous()

    db.init_app(app)

    from flask_wtf.csrf import CsrfProtect
    CsrfProtect(app)

    return app
