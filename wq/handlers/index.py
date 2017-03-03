#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from tornado import escape
from .base import BaseHandler
from ..methods.db import select_table, select_columns


class IndexHandler(BaseHandler):

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
                # 明文存cookie
                # self.set_cookie(username, db_pwd)
                # 密文存, 获取直接用self.get_secure_cookie(username)
                self.set_secure_cookie(username)
                self.write(username)
            else:
                self.write('Sorry, your password is wrong!')
        else:
            self.write('This user is not exist.')

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie('user', escape.json_encode(user))
        else:
            self.write('-1')


class ErrorHandler(BaseHandler):

    def get(self):
        self.render('error.html')

