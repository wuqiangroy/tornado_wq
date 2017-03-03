#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from tornado import escape, web
from .base import BaseHandler
from ..methods.db import select_table


class UserHandler(BaseHandler):

    @web.authenticated
    def get(self):
        # username = self.get_argument('user')
        username = escape.json_encode(self.current_user)
        user_infos = select_table(table='user', column='*',
                                  condition='username', value=username)
        self.render('user.html', users=user_infos)
