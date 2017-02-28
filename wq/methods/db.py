#!/usr/bin/env python
# _*_ coding:utf-8 _*_

"""
create db server
using MySQL
"""

import MySQLdb

conn = MySQLdb.connect(host='localhost', user='root', passwd='1234',
                       db='wuqiangroy', port=3306, charaset='utf8')
cur = conn.cursor()
