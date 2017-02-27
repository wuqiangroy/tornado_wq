#!/usr/bin/env python
# _*_ coding:utf-8 _*_

"""
使用安全cookie
"""

from tornado import httpserver, web, options, ioloop

options.define('port', default=8000, help='run on this given port', type=int)


class MainHandler(web.RequestHandler):

    def get(self):
        cookie = self.get_secure_cookie('count')
        # 应用将渲染一个统计浏览器中页面被加载次数的页面。
        # 如果没有设置cookie（或者cookie已经被篡改了），
        # 应用将设置一个值为1的新cookie。否则，应用将从cookie中读到的值加1。
        count = int(cookie) + 1 if cookie else 1

        CountString = '1 time' if count == 1 else '%d times' % count

        self.set_secure_cookie('count', str(count))

        self.write(
            "<html><head><title>Cooke Counter</title></head>"
            "<body><h1>You've viewed this page %s times.</h1>" % CountString +
            "</body></html>"
        )

if __name__ == '__main__':
    options.parse_command_line()

    settings = {
        'cookie_secure': 'x6FjQb8ERuiBYLhE6aruaCw/HIYp4UjEgoJycnUoT6o='
    }
    app = web.Application([
        (r'/', MainHandler)
    ], **settings)
    http_server = httpserver.HTTPServer(app)
    http_server.listen(options.options.port)
    ioloop.IOLoop.instance().start()
