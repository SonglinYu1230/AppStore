#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by why001 on 14/05/2017

import datetime
from flask import request, session, render_template, \
    url_for, abort, Response, jsonify, redirect, g, json
from flask_login import login_user, logout_user, login_required, current_user
from .util import IPAPKParser
from .util import FileManager
from . import main
from .. import db
from ..models import User, App, AppVersionInfo


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
            session['user_id'] = user.id
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
    user_id = session.get('user_id')
    apps = App.query.filter_by(owner=user_id).all()
    appList = []
    for app in apps:
        appList.append(app.convert_to_dict())

    response = {
        'isOk': True,
        'apps': appList
    }
    return jsonify(response)

@main.route('/parseAppInfo', methods=['POST'])
@login_required
def parse_app_Info():
    platform_type = request.form['platformType']
    response = None
    if platform_type == 'iOS':
        response = parse_plist_info(request.files['plist'])
    elif platform_type == 'Android':
        parse_xml_info(request.files['xml'])
        parse_arsc_info(request.files['arsc'])
    else:
        return 'Error'
    response['isOk'] = True
    return jsonify(response)


@main.route('/uploadApp', methods=['POST'])
@login_required
def app_upload():
    form = request.form
    user_id = session.get('user_id')
    platform_type = form['platformType']
    app_id = form['appID']
    version_number = form['versionNumber']
    save_result = FileManager.save_user_file(user_id, platform_type,
                                             app_id, version_number, request.files['app'])

    if save_result:
        app = App.query.filter_by(id=app_id).first()
        create_time = datetime.datetime.now()
        if not app:
            app = App(id=app_id,
                      name=form['appName'],
                      app_platform=platform_type,
                      owner=int(user_id),
                      create_time=create_time
                      )
            db.session.add(app)
        app_version = AppVersionInfo.query.filter_by(build=version_number, version=form['versionCode'], app_id=app_id).first()
        if not app_version:
            app_version = AppVersionInfo(build=version_number,
                                         version=form['versionCode'],
                                         update_log=form['updateLog'],
                                         create_time=create_time,
                                         app_id=app_id
                                         )
            db.session.add(app_version)
        else:
            app_version.update_log = 'Testtttttt'
            app_version.create_time = create_time
            db.session.merge(app_version)
        db.session.commit()
    else:
        pass

    return jsonify({'status': 'OK'})


def parse_plist_info(plist_file):
    temp_path = FileManager.save_temp_file(plist_file, session.get('_id'))
    print(temp_path)
    with open(temp_path, 'rb') as f:
        return IPAPKParser.plist_info(f.read())

def parse_xml_info():
    pass

def parse_arsc_info():
    pass