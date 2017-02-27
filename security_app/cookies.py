#!/usr/bin/env python
# _*_ coding:utf-8 _*_

"""
存储在安全cookie里的用户名标识一个人。当某人首次在某个浏览器（或cookie过期后）访问我们的页面时，
我们展示一个登录表单页面。表单作为到LoginHandler路由的POST请求被提交。
post方法的主体调用set_secure_cookie()来存储username请求参数中提交的值。
"""

import os
from tornado import web, httpserver, ioloop, options

options.define('port', default=8000, help='run on this given port', type=int)


class BaseHandler(web.RequestHandler):

    def get_current_user(self):
        return self.get_secure_cookie('username')


class LoginHandler(BaseHandler):

    def get(self):
        self.render('login.html')

    def post(self):
        self.set_secure_cookie('username', self.get_argument('username'))
        self.redirect('/')


class WelcomeHandler(BaseHandler):

    @web.authenticated
    def get(self):
        self.render('index.html', user=self.current_user)


class LogoutHandler(BaseHandler):

    def get(self):
        if (self.get_argument('logout', None)):
            self.clear_cookie('username')
            self.redirect('/')

if __name__ == '__main__':
    options.parse_command_line()

    settings = {
        'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
        'cookie_secret': 'x6FjQb8ERuiBYLhE6aruaCw/HIYp4UjEgoJycnUoT6o=',
        # 设置XSRF保护
        'xsrf_cookies': True,
        'login_url': '/login',
    }

    app = web.Application([
        (r'/', WelcomeHandler),
        (r'/login', LoginHandler),
        (r'logout', LogoutHandler),
    ], **settings)

    http_server = httpserver.HTTPServer(app)
    http_server.listen(options.options.port)
    ioloop.IOLoop.instance().start()
