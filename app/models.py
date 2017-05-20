#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by why001 on 14/05/2017

from . import db, login_manager
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __table__name = 'users'
    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)
    nick_name = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True)
    wechat = db.Column(db.String(64), unique=True)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

    # def __repr__(self):
    #     return '<User %>' % self.name


class App(db.Model):
    __table__name = 'apps'
    id = db.Column(db.String(64), nullable=False, primary_key=True)
    name = db.Column(db.String(16), nullable=False)
    desc = db.Column(db.Text)
    app_platform = db.Column(db.String(16), nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    create_time = db.Column(db.DateTime())
    download_count = db.Column(db.Integer)


class AppVersionInfo(db.Model):
    __table__name = 'app_version_info'
    build = db.Column(db.String(64), nullable=False, primary_key=True)
    version = db.Column(db.String(64), nullable=False, primary_key=True)
    update_log = db.Column(db.Text)
    download_url = db.Column(db.String(64))
    create_time = db.Column(db.DateTime())
    app_id = db.Column(db.String(64), db.ForeignKey('app.id'), nullable=False, primary_key=True)
    download_count = db.Column(db.Integer)


class Group(db.Model):
    __table__name = 'groups'
    user_name = db.Column(db.String(64), db.ForeignKey('user.name'), nullable=False, primary_key=True)
    group_id = db.Column(db.String(64), nullable=False, primary_key=True)
