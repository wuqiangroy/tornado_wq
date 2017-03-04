#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import time
from base import BaseHandler


class SleepHandler(BaseHandler):

    def get(self):
        time.sleep(17)
        self.render('sleep.html')


class SeeHandler(BaseHandler):

    def get(self):
        self.render('see.html')