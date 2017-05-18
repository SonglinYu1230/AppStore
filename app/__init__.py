#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by why001 on 14/05/2017

from flask import Flask
from flask_sqlalchemy  import SQLAlchemy
from config import config
from flask_login import LoginManager

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'basic'
login_manager.login_view = 'main.login'

def create_app(config_name):
    app = Flask(__name__, static_folder='./static', template_folder='./templates')
    app.config.from_object(config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    login_manager.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # 附加路由和自定义的错误页面
    from .main import main as main_blueprint
    from .main import auth as auth_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)

    return app