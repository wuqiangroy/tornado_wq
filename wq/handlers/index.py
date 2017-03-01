#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from tornado import web
from ..methods.db import select_table, select_columns


class IndexHandler(web.RequestHandler):

    def get(self):
        usernames = select_columns(table='users', column='username')
        one_user = usernames[0][0]
        self.render('index.html', user=one_user)

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        user_infos = select_table(table='users', column='*',
                                  condition='username', value=username)
        if user_infos:
            db_pwd = user_infos[0][2]
            if db_pwd == password:
                self.write('Welcome you:' + username)
            else:
                self.write('Sorry, your password is wrong!')
        else:
            self.write('This user is not exist.')
