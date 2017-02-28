#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from tornado import web


class IndexHandler(web.RequestHandler):

    def get(self):
        self.render('index.html')