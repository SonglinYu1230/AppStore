#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by why001 on 16/05/2017

import inspect
from flask import request

def who_am_i():
    # print(inspect.stack()[1][3])
    pass

def before_app_first_request():
    print(who_am_i())

def before_app_request():
    print(who_am_i())

def before_request():
    # print()
    print(request.url)
    print(who_am_i())
