#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from tornado import web
from ..methods.db import select_table


class UserHandler(web.RequestHandler):

    def get(self):
        username = self.get_argument('user')
        user_infos = select_table(table='user', column='*',
                                  condition='username', value=username)
        self.render('user.html', users=user_infos)