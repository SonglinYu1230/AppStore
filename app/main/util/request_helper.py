#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by why001 on 03/06/2017


def os_type(user_agent):
    if 'iOS' in user_agent or 'iPhone' in user_agent or 'iPad' in user_agent:
        return 'iOS'
    elif 'Android' in user_agent:
        return 'Android'
    else:
        return 'Other'