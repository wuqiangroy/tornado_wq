#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from tornado import httpserver, options, ioloop, web

options.define('port', default=8080, help='run this given port', type=int)


class IndexHandler(web.RequestHandler):

    def get(self):
        greeting = self.get_argument('greeting', 'Hello')
        self.write(greeting + ', friendly user!')

    def write_error(self, status_code, **kwargs):
        self.write(u'出错啦！你导致了%d错误。' % status_code)


if __name__ == '__main__':
    options.parse_command_line()
    app = web.Application(handlers=[(r'/', IndexHandler)])
    http_server = httpserver.HTTPServer(app)
    http_server.listen(options.options.port)
    ioloop.IOLoop.instance().start()
