#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import time
from tornado import web, ioloop, gen
from base import BaseHandler


class SleepHandler(BaseHandler):

    @web.asynchronous
    def get(self):
        ioloop.IOLoop.instance().add_timeout(time.time()+17, callback=
                                             self.on_response)

    def on_response(self):
        self.render('sleep.html')
        self.finish()
"""
class SleepHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        yield gen.Task(ioloop.IOLoop.instance().add_timeout,
                       time.time()+17)
        self.render("sleep.html')
"""


class SeeHandler(BaseHandler):

    def get(self):
        self.render('see.html')
