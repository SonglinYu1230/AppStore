#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by why001 on 14/05/2017

from . import db

class User(db.Model):
    __table__name = 'user'
    id = db.Column(db.String(64), nullable=False, unique=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)
    nick_name = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True)
    wechat = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<User %>' % self.name

class App(db.Model):
    __table__name = 'app'
    id = db.Column(db.String(64), unique=True, nullable=False, primary_key=True)
    name = db.Column(db.String(16), nullable=False)
    desc = db.Column(db.Text)
    app_platform = db.Column(db.String(16), nullable=False)
    owner = db.Column(db.String(64), db.ForeignKey('user.id'), nullable=False)
    create_time = db.Column(db.Time())

    def __repr__(self):
        return '<App %>' % self.id

class AppVersion(db.Model):
    __table__name = 'app_version'
    build = db.Column(db.String(64), nullable=False, primary_key=True)
    version = db.Column(db.String(64), nullable=False, primary_key=True)
    update_log = db.Column(db.Text)
    download_url = db.Column(db.String(64))
    create_time = db.Column(db.Time())
    app_id = db.Column(db.String(64), db.ForeignKey('app.id'), nullable=False, primary_key=True)

    def __repr__(self):
        return '<build %>' % self.build

class Group(db.Model):
    __table__name = 'group'
    user_name = db.Column(db.String(64), db.ForeignKey('user.name'), nullable=False, primary_key=True)
    group_id = db.Column(db.String(64), nullable=False, primary_key=True)

    def __repr__(self):
        return '<Group %>' % self.group_id