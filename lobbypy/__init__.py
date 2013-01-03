import os
from socketio.server import SocketIOServer
from flask import Flask
from lobbypy.utils import db, mako, oid, cache

def create_app():
    return Flask(__name__)

def config_app(app, **config):
    app.secret_key = (config.get('SESSION_KEY', None)
            or os.environ['SESSION_KEY'])
    app.config['SQLALCHEMY_DATABASE_URI'] = (
            config.get('SQLALCHEMY_DATABASE_URI', None)
            or os.environ['SQLALCHEMY_DATABASE_URI'])
    app.debug = config.get('DEBUG', False)
    app.config['TESTING'] = config.get('TESTING', False)
    app.config['RCON_CHECK_SERVER'] = config.get('RCON_CHECK_SERVER', True)
    app.config['CACHE_TYPE'] = config.get('CACHE_TYPE', 'null')
    if app.config['CACHE_TYPE'] == 'redis':
        app.config['CACHE_REDIS_HOST'] = config['CACHE_REDIS_HOST']
        app.config['CACHE_REDIS_PORT'] = config.get('CACHE_REDIS_PORT', None)
        app.config['CACHE_REDIS_PASSWORD'] = config.get('CACHE_REDIS_PASSWORD',
                None)
    ADMIN_URL = config.get('ADMIN_URL', '/admin')
    app.config['MAX_AUTH_ATTEMPTS'] = config.get('MAX_AUTH_ATTEMPTS', 5)

    mako.init_app(app)
    db.init_app(app)
    cache.init_app(app)
    oid.init_app(app)
    from lobbypy import models
    from lobbypy import views

    app.add_url_rule('/', view_func=views.index)
    app.add_url_rule('/login', view_func=views.login)
    app.add_url_rule('/logout', view_func=views.logout)
    app.add_url_rule(ADMIN_URL, view_func=views.admin, methods=['GET', 'POST'])
    app.add_url_rule('/socket.io/<path:path>', view_func=views.run_socketio)
    app.before_request(views.before_request)
