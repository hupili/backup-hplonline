# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from pyquery import PyQuery as pq

d = pq(open(sys.argv[1]).read())
print d('#blog_text').html()
