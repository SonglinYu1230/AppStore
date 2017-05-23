#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by why001

import sys
import os
import re
import shutil
import zipfile
import plistlib
import xml.etree.ElementTree as ET
from . import apk


def ipa_name_from_arguments():
    argvs = sys.argv
    ipa_name = None
    if len(argvs) >= 2:
        ipa_name = argvs[1]
    else:
        print('please input the name of ipa or apk!')
        print('for exmaple: python ipaparser.py google.ipa')
    return ipa_name


def plist_path_with_ipa_path(ipa_path):
    ipa_file = zipfile.ZipFile(ipa_path)
    name_list = ipa_file.namelist()

    regex = re.compile(r'Payload/[^/]+.app/Info.plist')
    result = list(filter(regex.search, name_list))
    if result:
        return result[0]


def plist_info_with_path(plist_path, ipa_path):
    ipa_file = zipfile.ZipFile(ipa_path)
    plist_data = ipa_file.read(plist_path)
    plist_root = plistlib.loads(plist_data)
    return plist_root


def info_of_plist_property(plist_info, property_name):
    value = plist_info[property_name]
    print(property_name + ' is ' + str(value))
    return value


def plist_info(plist_path):
    # plist_file = zipfile.ZipFile(plist_path)
    # plist_data = plist_file.read(plist_path)
    plist_root = plistlib.loads(plist_path)
    version_number =   plist_root['CFBundleVersion']
    builder_number =  plist_root['CFBundleShortVersionString']
    app_name = plist_root['CFBundleDisplayName']
    bundle_id = plist_root['CFBundleIdentifier']
    return {
        'version_number': version_number,
        'builder_number': builder_number,
        'app_name': app_name,
        'bundle_id': bundle_id
    }


def parse_miniapk_with_path(apk_path):
    head, tail = os.path.split(apk_path)
    os.chdir(head)
    apktool_cmd = 'apktool d ' + apk_path
    os.system(apktool_cmd)
    path, extension = os.path.splitext(apk_path)

    binary_xml_path = os.path.join(path, 'original/AndroidManifest.xml')
    parse_info = parse_binary_xml_path(binary_xml_path)

    name_xml_path = os.path.join(path, 'res/values/strings.xml')
    parse_info['app_name'] = app_name_with_xml_path(name_xml_path)
    shutil.rmtree(path)
    return parse_info

def convert_xml(binary_xml_path, text_xml_path):
    ap = apk.AXMLPrinter(open(binary_xml_path, "rb").read())
    buff = ap.get_xml_obj().toprettyxml()

    fd = open(text_xml_path, "w")
    fd.write( buff )
    fd.close()


def parse_xml(xml_path):
    tree = ET.ElementTree(file=xml_path)
    root = tree.getroot()
    version_code = root.attrib["{http://schemas.android.com/apk/res/android}versionCode"]
    version_name = root.attrib["{http://schemas.android.com/apk/res/android}versionName"]
    package = root.attrib['package']

    return {
        'version_number': version_name,
        'builder_number': version_code,
        'bundle_id': package
    }


def parse_binary_xml_path(xml_path):
    ap = apk.AXMLPrinter(open(xml_path, "rb").read())
    buff = ap.get_xml_obj().toprettyxml()

    fd = open(xml_path, "w")
    fd.write(buff)
    fd.close()

    return parse_xml(xml_path)


def app_name_with_xml_path(xml_path):
    tree = ET.ElementTree(file=xml_path)
    app_name = ''
    # 理论情况下只有一个app_name
    for elem in tree.iterfind("string[@name='app_name']"):
        app_name = elem.text
    return app_name
