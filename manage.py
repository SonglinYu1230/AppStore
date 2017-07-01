#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by why001 on 14/05/2017
# 用于启动程序以及其它的程序任务

from app import create_app, db
from app.models import User, App, AppVersionInfo, Group # 在这里导入，不然创建的database没有表, 20170603
from flask_script import Manager, Server, Shell
from flask_migrate import Migrate, MigrateCommand
from config import base_dir
# from OpenSSL import SSL

# context = SSL.Context(SSL.SSLv23_METHOD) #TLSv1_2_METHOD
key_path = base_dir + '/static/server.key'
crt_path = base_dir + '/static/server.crt'
context = (crt_path, key_path)

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)
server = Server(host='0.0.0.0', port=5000, use_debugger=True, ssl_context=context)

def make_shell_context():
    return dict(app=app, db=db, User=User, App=App, AppVersionInfo=AppVersionInfo, Group=Group)
manager.add_command("shell", Shell(make_context=make_shell_context()))
manager.add_command("runserver", server)
manager.add_command('db', MigrateCommand)
# manager.add_command('ssl_context', 'adhoc')

if __name__ == '__main__':
    manager.run()