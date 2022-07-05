from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import DevelopmentConfig
from flask_login import LoginManager, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from os.path import join, dirname, realpath
import os

# from flask_mysqldb import MySQL
# import MySQLdb.cursors

db = SQLAlchemy()
migrate = Migrate()
BASEDIR = os.path.abspath(os.path.dirname(realpath(__file__)))
UPLOAD_FOLDER_DCC = os.path.join(BASEDIR, './static/files/dcc')
UPLOAD_FOLDER_METRO = os.path.join(BASEDIR, './static/files/metro')

def app_edoc(config=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    db.app = app

    migrate.init_app(app, db)
    migrate.app = app

    from app_edoc.dcc.autentikasi import model_autentikasi, controller_autentikasi

    admin = Admin(app, name='Control Panel Admin', template_mode='bootstrap4', index_view=model_autentikasi.DashboardView())
    admin.add_view(model_autentikasi.Controller(model_autentikasi.User, db.session, name='User'))
    # admin.add_view(ModelView(model_elo.m_jenis_kawat, db.session, name='Jenis Kawat'))

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'autentikasi.login'

    from app_edoc.dcc.autentikasi import model_autentikasi

    @login_manager.user_loader
    def load_user(user_id):
        return model_autentikasi.User.query.get(int(user_id))

    # ---------------------- REGISTER BLUEPRINT -------------------- 

    from app_edoc.dcc.autentikasi import bp_autentikasi as autentikasi
    app.register_blueprint(autentikasi)
    from app_edoc.dcc.dokumen import bp_dokumen as dokumen
    app.register_blueprint(dokumen)
    
    # db.create_all()

    return app