#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by why001 on 16/05/2017

import inspect
from flask import request

def who_am_i():
    return inspect.stack()[1][3]


def before_app_first_request():
    # print('*' * 20 + who_am_i() + '    start' + '*' * 20)
    # print(request)
    # print(request.headers)
    # print(request.form)
    # print(request.data)
    # print(request.files)
    # print('*' * 20 + who_am_i() + '    end' + '*' * 20)
    pass


def before_app_request():
    # print('*' * 20 + who_am_i() + '    start' + '*' * 20)
    # print(request)
    # print(request.headers)
    # print(request.form)
    # print(request.data)
    # print(request.files)
    # print('*' * 20 + who_am_i() + '    end' + '*' * 20)
    pass


def before_request():
    print('*' * 20 + who_am_i() + '    start' + '*' * 20)
    print(request.url)
    print(request.headers)
    print('*' * 20 + who_am_i() + '    end' + '*' * 20)
