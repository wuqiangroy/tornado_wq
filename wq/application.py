#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import os
from tornado import web
from url import url

settings = {
    'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
    'static_path': os.path.join(os.path.dirname(__file__), 'statics'),
    'cookie_secret': "Qdbk+l5DSz6XOw9zBCSYKA==",
    'xsrf_cookies': True,
    'login_url': '/',
}

application = web.Application(
    handlers=url,
    **settings
)
