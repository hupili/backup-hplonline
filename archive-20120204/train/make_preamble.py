# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import pickle
import os

data = pickle.loads(open('data.pickle').read())

template = '''---
layout: post
title: "%s"
date: %s
comments: true
categories: tech
tags: %s
_baiduhi_id: %s
---
'''

fn = sys.argv[1]

info = data[fn]

for k in info:
    info[k] = info[k].strip()

info['category'] = info['category'].replace('类别：', '')
info['category'] = info['category'].replace('&#47;', '&')

tags = '[' + ','.join(map(lambda x: '"' + x + '"', info['category'].split('&'))) + ']'

print template % (info['title'], info['date'], tags, fn)
