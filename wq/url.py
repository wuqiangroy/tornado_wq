#!/usr/bin/env python
# _*_ coding:utf-8 _*_

"""
The url structure of website
"""

import sys
from handlers.index import IndexHandler
from handlers.sleep import SleepHandler, SeeHandler

reload(sys)
sys.setdefaultencoding('utf-8')

url = [
    (r'/', IndexHandler),
    (r'/sleep', SleepHandler),
    (r'/see', SeeHandler),
]

