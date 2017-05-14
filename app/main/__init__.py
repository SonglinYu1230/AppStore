#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by why001 on 14/05/2017

from flask import Blueprint

main = Blueprint('main', __name__)

# 在此处导入是为了避免循环导入依赖，因为在views.py和errors.py中还要导入蓝本main
from . import views, errors
