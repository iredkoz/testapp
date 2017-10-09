import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_marshmallow import Marshmallow

from config import app_config

UPLOAD_FOLDER = '/var/uploads/'

db = SQLAlchemy()
ma = Marshmallow()

def create_app(config_name):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI']='mysql://ilya:ilya@localhost/testapp?charset=utf8'
    app.config['SQLALCHEMY_BINDS']={'recipe':'mysql://ilya:ilya@localhost/recipe?charset=utf8'}
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']='False'
    app.debug = True
    app.secret_key='super secret key'
    
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    Bootstrap(app)
    db.init_app(app)
    migrate = Migrate(app, db)
    
    from app import models

    from .finance import finance as finance_blueprint
    app.register_blueprint(finance_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from .recipeapp import recipeapp as recipeapp_blueprint
    app.register_blueprint(recipeapp_blueprint)

    from .shopapp import shopapp as shopapp_blueprint
    app.register_blueprint(shopapp_blueprint)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html')

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('errors/500.html')

    return app
