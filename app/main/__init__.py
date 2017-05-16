#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by why001 on 14/05/2017

from flask import Blueprint, request
from .common import *

main = Blueprint('main', __name__)
# main.before_app_first_request(before_app_first_request)
main.before_app_request(before_app_request)
main.before_request(before_request)

@main.after_request
def after_request(response):
    print(who_am_i())
    print(request.url)
    response.headers['key'] = 'value'
    return response

# 在此处导入是为了避免循环导入依赖，因为在views.py和errors.py中还要导入蓝本main
from . import views, errors
