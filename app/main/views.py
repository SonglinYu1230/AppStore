#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by why001 on 14/05/2017

import datetime
import os
from flask import request, session, render_template, \
    url_for, abort, Response, jsonify, redirect, g, json
from flask_login import login_user, logout_user, login_required, current_user
from .util import IPAPKParser
from .util import FileManager
from . import main, app_file
from .. import db
from ..models import User, App, AppVersionInfo


@main.route('/favicon.ico')
def favicon():
    return url_for('static', filename='images/favicon.ico')


@main.route('/')
@login_required
def index():
    return redirect('/home')


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/home')
    else:
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            user_info = request.form
            user_name = user_info['username']
            password = user_info['password']
            if user_name and password:
                user = User.query.filter_by(name=user_name, password=password).first()
                if user:
                    login_user(user, True)
                    session['user_id'] = user.id
                    # return redirect(url_for('main.home'))

                    return jsonify(
                        isOk=True
                    )
            return jsonify(
                isOk=False,
                errMsg='user not found'
            )
        else:
            return abort(400)


@main.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/home')
# @login_required
def home():
    return render_template('homepage.html')


@main.route('/apps', methods=['GET', 'POST'])
@login_required
def apps():
    if (request.method == 'GET'):
        return render_template('apps.html')

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
    response = {}
    if platform_type == 'iOS':
        response.update(parse_plist_info(request.files['plist']))
    elif platform_type == 'Android':
        response.update(parse_miniAPK(request.files['miniAPK'], request.form['fileName']))
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



@app_file.route('/test')
def static_file_parser():
    print('this is it')
    return jsonify(
        isOk=True
    )


def parse_plist_info(plist_file):
    temp_path = FileManager.save_blob_file(plist_file, 'blob', session.get('_id'))

    with open(temp_path, 'rb') as f:
        parse_result = IPAPKParser.plist_info(f.read())
        os.remove(temp_path)
        return parse_result

def parse_miniAPK(miniAPK, file_name):
    temp_path = FileManager.save_blob_file(miniAPK, file_name, session.get('_id'))
    parse_result = IPAPKParser.parse_miniapk_with_path(temp_path)
    os.remove(temp_path)
    return parse_result

def parse_xml_info(binary_xml_file):
    temp_binary_xml_path = FileManager.save_temp_file(binary_xml_file, session.get('_id'))
    parse_result = IPAPKParser.parse_binary_xml_path(temp_binary_xml_path)
    os.remove(temp_binary_xml_path)
    return parse_result


def parse_arsc_info():
    pass