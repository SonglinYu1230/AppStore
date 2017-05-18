#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by why001 on 14/05/2017

from flask import request, session, render_template, \
    url_for, abort, Response, jsonify, redirect, g
from flask_login import login_user, logout_user, login_required, current_user

from . import main
from .. import db
from ..models import User


@main.route('/')
@login_required
def index():
    return redirect('/home')


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/home')
    else:
        return render_template('login.html')


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))


@main.route('/session', methods=['POST'])
def set_session():
    loginDict = request.json
    if loginDict:
        user = User.query.filter_by(name=loginDict['username'], password=loginDict['password']).first()
        if user:
            login_user(user, True)
            # session['user_name'] = loginDict['username']
            # response = jsonify(
            #     isOk=True
            # )
            response = {
                'isOk': True
            }

            # response.status_code = 302
            # response.headers['Location'] = url_for('main.home')
            # headers = {
            #     'Location': url_for('main.home')
            # }
            # return Response(url_for('main.home'), response=response, status=302, headers=headers)
            return redirect(url_for('main.home'))
    return jsonify(
        isOk=False,
        errMsg='user not found'
    )


@main.route('/home')
@login_required
def home():
    return render_template('homepage.html')


@main.route('/apps')
@login_required
def apps():
    return 'Only authenticated users are allowed!'
    user_name = session['user_name']
    pass


@main.route('/parseAppInfo', methods=['POST'])
@login_required
def parse_app_Info():
    pass


@main.route('/appUpload', methods=['POST'])
@login_required
def app_upload():
    print(request)
    print(request.form)
    print('request.files')
    print(request.files)
    imfile = request.files['ipa']
    imfile.save("/Users/Yu/Desktop/1.ipa")
    print(request.content_length)
    return jsonify({'status': 'OK'})


@main.route('/user/<name>')
def user(name):
    return render_template('page.html', user=name)
    # if name == 'baidu':
    #     return redirect('https://www.baidu.com')
    # elif name == 'google':
    #     return redirect('https://www.google.com/ncr')
    # elif name == 'NO':
    #     return abort(404)
    # return '<h1> Hello, %s <h1>' % name
