#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from tornado import web


class BaseHandler(web.RequestHandler):

    def get_current_user(self):
        return self.get_secure_cookie('user')
