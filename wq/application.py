#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import os
from tornado import web
from url import url

settings = {
    'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
    'static_path': os.path.join(os.path.dirname(__file__), 'statics')
}

application = web.Application(
    handlers=url,
    **settings
)
