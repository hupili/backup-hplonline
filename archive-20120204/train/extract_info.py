# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import pickle
from scrapely import Scraper
s = Scraper()

url1='ab4bc711263c261eb8127bcb.html'
data={
    'title': 'pthread对多线程访问全局数据结构的支持',
    'date': '2010-09-20  22:03',
    'category': '类别：Linux'
        }

if len(sys.argv) > 1:
    url2=sys.argv[1]
else:
    url2='fa2ebd45db2fd724cefca317.html'

#import pprint
##pp = pprint.Prettyprint(indent=2)
#pprint.pprint(d)
#print d[0]['title'][0]
#print d[0]['category'][0]
#print d[0]['date'][0]

s.train(url1, data)

import os

data = {}

#for dirname, dirnames, filenames in os.walk('../utf8/'):
#    for filename in filenames:

for fn in os.listdir('../utf8/'):
    print fn
    url2 = '../utf8/' + fn
    d = s.scrape(url2)
    try:
        data[fn] = {
                'title': unicode(d[0]['title'][0]),
                'category': unicode(d[0]['category'][0]),
                'date': unicode(d[0]['date'][0])
            }
    except Exception as e:
        print e

open('data.pickle', 'w').write(pickle.dumps(data))

