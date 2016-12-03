#! ../env/bin/python
import os
import random
import string

from flask import Flask, render_template, current_app, url_for, redirect
from flask_security import SQLAlchemyUserDatastore, login_user
from webassets.loaders import PythonLoader as PythonAssetsLoader
from werkzeug import url_decode

from shell.webinterface import assets
from shell.webinterface.controllers.user.models import User, Role, Connection
from shell.webinterface.extensions import (
    db,
    cache,
    assets_env,
    bootstrap,
    debug_toolbar,
    security,
    social
)
from shell.webinterface.controllers.user import forms
from shell.webinterface.plugin.social import SQLAlchemyConnectionDatastore
from shell.webinterface.plugin.social.utils import get_connection_values_from_oauth_response
from shell.webinterface.plugin.social.views import connect_handler
from shell.webinterface.plugin.social.signals import login_failed


class MethodRewriteMiddleware(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        if 'METHOD_OVERRIDE' in environ.get('QUERY_STRING', ''):
            args = url_decode(environ['QUERY_STRING'])
            method = args.get('__METHOD_OVERRIDE__')
            if method:
                method = method.encode('ascii', 'replace')
                environ['REQUEST_METHOD'] = method
        return self.app(environ, start_response)


def create_app(object_name, env="prod"):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/
    Arguments:
        object_name: the python path of the config object,
                     e.g. appname.settings.ProdConfig
        env: The name of the current environment, e.g. prod or dev
    """

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    app = Flask(
        __name__,
        static_folder=os.path.join(BASE_DIR, 'webinterface', 'static'),
        template_folder=os.path.join(BASE_DIR, 'webinterface', 'templates')
    )

    # Allow method override
    app.wsgi_app = MethodRewriteMiddleware(app.wsgi_app)

    app.config.from_object(object_name)
    app.config['ENV'] = env
    app.jinja_env.globals['project_name'] = '{{ project_name }}'

    # register flask extensions
    register_extensions(app)

    # register our blueprints
    register_blueprints(app)

    # register authentication singal handlers
    register_authentication_signal_handlers(app)

    register_errorhandlers(app)
    return app

def register_extensions(app):
    # initialize SQLAlchemy
    db.init_app(app)    
    # initialize the cache
    cache.init_app(app)

    # initialize security
    ds = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, datastore=ds,
                      register_form=forms.ExtendedRegisterForm)   
    # initialize bootstrap resource
    bootstrap.init_app(app)
    # initialize the debug tool bar
    #debug_toolbar.init_app(app)

    # Initialize social
    social_ds = SQLAlchemyConnectionDatastore(db, Connection)
    social.init_app(app, social_ds)

    #Import and register the different asset bundles
    assets_env.init_app(app)
    assets_loader = PythonAssetsLoader(assets)
    for name, bundle in assets_loader.load_bundles().iteritems():
        assets_env.register(name, bundle)
    return None


def register_blueprints(app):
    from shell.webinterface.controllers.main import main
    app.register_blueprint(main)
    from shell.webinterface.controllers.user import user
    app.register_blueprint(user)
    return None


def register_authentication_signal_handlers(app):
    @login_failed.connect_via(app)
    def on_login_failed(sender, provider, oauth_response):
        connection_values = get_connection_values_from_oauth_response(provider, oauth_response)
        ds = current_app.extensions['security'].datastore
        chars = string.ascii_letters + string.digits + '!@#$%^&*()'
        random.seed = (os.urandom(1024))
        user_kwargs = dict(username = connection_values['display_name'] or \
                                      "_".join(connection_values['full_name'].split()) or \
                                    connection_values['email'].split("@")[1],
                            # have to get a silly email address
                            email = connection_values['email'] or "123@abc.com",
                            password = ''.join(random.choice(chars) for i in range(10)))
        user = ds.create_user(**user_kwargs) #fill in relevant stuff here
        ds.commit()
        connection_values['user_id'] = user.id
        connect_handler(connection_values, provider)
        login_user(user)
        current_app.extensions['sqlalchemy'].db.session.commit()
        return redirect(url_for('main.home'))

def register_errorhandlers(app):
    def render_error(error):
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template("{0}.html".format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None
