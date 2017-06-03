#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by why001 on 14/05/2017

from flask import Blueprint, request
from .common import *
from config import base_dir


main_static_folder = base_dir + '/app/static'
main_template_folder = base_dir + '/app/templates'
app_file_template_folder = base_dir + '/AppFiles'

main = Blueprint('main', __name__, static_folder=main_static_folder, template_folder=main_template_folder)
auth = Blueprint('auth', __name__)
app_file = Blueprint('app_file', __name__, static_folder=app_file_template_folder)

# main.before_app_first_request(before_app_first_request)
main.before_app_request(before_app_request)
main.before_request(before_request)

@main.after_request
def after_request(response):
    print(who_am_i())
    print('*******************after_request start************************')
    print(request)
    print(response)
    print('*******************after_request end************************')
    return response

# 在此处导入是为了避免循环导入依赖，因为在views.py和errors.py中还要导入蓝本main
from . import views, errors
