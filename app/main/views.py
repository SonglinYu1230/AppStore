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
from .util import request_helper


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
@login_required
def home():
    return render_template('homepage.html')


@main.route('/apps', methods=['GET', 'POST'])
@login_required
def apps():
    if (request.method == 'GET'):
        return render_template('apps.html')

    # TODO: 区分是否登录
    apps = []
    user_agent = request.headers.get('User-Agent')
    if 'iOS' in user_agent or 'iPhone' in user_agent or 'iPad' in user_agent:
        apps = App.query.filter_by(app_platform='iOS').all()
        pass
    elif 'Android' in user_agent:
        apps = App.query.filter_by(app_platform='Android').all()
        pass
    else:
        user_id = session.get('user_id')
        apps = App.query.filter_by(owner=user_id).all()
        pass

    appList = []
    for app in apps:
        appList.append(app.convert_to_dict())

    response = {
        'isOk': True,
        'apps': appList
    }
    return jsonify(response)

@main.route('/store/apps', methods=['GET', 'POST'])
def store_apps():
    if (request.method == 'GET'):
        return render_template('apps.html')

    request.headers.get('User-Agent')

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

@main.route('/appversion', methods=['GET', 'POST'])
def version_info():
    if (request.method == 'GET'):
        return render_template('appversion.html')

    user_agent = request.headers.get('User-Agent')
    platform_type = request_helper.os_type(user_agent)

    apps = AppVersionInfo.query.filter_by(app_platform=platform_type,app_id=request.form.get('appID')).all()
    # request.headers.get('User-Agent')
    #
    # user_id = session.get('user_id')
    # apps = App.query.filter_by(owner=user_id).all()
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
    platform_type = form.get('platformType')
    app_id = form.get('appID')
    version_number = form.get('versionNumber')
    version_code = form.get('versionCode')
    save_result = FileManager.save_user_file(user_id, platform_type,
                                             app_id, version_number, request.files['app'])

    if save_result:
        app = App.query.filter_by(id=app_id).first()
        create_time = datetime.datetime.now()
        if not app:
            app = App(id=app_id,
                      name=form.get('appName'),
                      app_platform=platform_type,
                      owner=int(user_id),
                      create_time=create_time
                      )
            db.session.add(app)
        app_version = AppVersionInfo.query.filter_by(build=version_number, version=version_code, app_id=app_id).first()
        if not app_version:
            app_version = AppVersionInfo(app_platform=platform_type,
                                         build=version_number,
                                         version=version_code,
                                         update_log=form.get('updateLog'),
                                         create_time=create_time,
                                         app_id=app_id
                                         )
            db.session.add(app_version)
        else:
            app_version.update_log = ''
            app_version.create_time = create_time
            db.session.merge(app_version)
        db.session.commit()

        app_version = AppVersionInfo.query.filter_by(app_platform=platform_type, app_id=app_id).order_by(AppVersionInfo.build.desc()).first()
        app_version = app_version.convert_to_dict()
        app_version['download_count'] = app.download_count

        app_version['isOk'] = True
        return jsonify(app_version)
    else:
        return jsonify(
            isOk=False
        )


@app_file.route('/test')
def static_file_parser():
    print('this is it')
    return jsonify(
        isOk=True
    )


def parse_plist_info(plist_file):
    temp_blob_path = FileManager.save_blob_file(plist_file, 'blob', session.get('_id'))
    temp_path = FileManager.get_plist_path(temp_blob_path)
    os.remove(temp_blob_path)
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