# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import pickle
import os

data = pickle.loads(open('data.pickle').read())

#for k, v in data.iteritems():
#    print v['category']


categories = ['类别：.net&#47;c#&#47;sql',
'类别：Asm',
'类别：Linux',
'类别：Math',
'类别：Matlab',
'类别：Network',
'类别：Scm',
'类别：Vb',
'类别：Vc',
'类别：c&#47;c++',
'类别：算法']


for k, v in data.iteritems():
    if v['category'] in categories:
        print k
