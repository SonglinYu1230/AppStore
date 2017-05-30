#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by why001 on 14/05/2017
# 用于启动程序以及其它的程序任务

import os
from app import create_app, db
from flask_script import Manager, Server
from flask_migrate import Migrate

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)
server = Server(host='0.0.0.0', port=5000, use_debugger=True)

# def make_shell_context():
#     return dict(app=app, db=db, User=User, Role=Role)
# manager.add_command("shell", Shell(make_context=make_shell_context()))
manager.add_command("runserver", server)
# manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()