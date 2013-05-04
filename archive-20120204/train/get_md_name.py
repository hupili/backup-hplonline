# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import pickle
import os

data = pickle.loads(open('data.pickle').read())

fn = sys.argv[1]

info = data[fn]
name = info['date'].split(' ')[0] + '-' + info['title'].strip() + '.md'
name = name.replace('/', '').replace(' ', '')
print name

