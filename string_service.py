#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from tornado import httpserver, ioloop, options, web
import textwrap


options.define('port', default=5000, help='run on this given port', type=int)


class ReverseHandler(web.RequestHandler):
    def get(self, input):
        self.write(input[::-1])


class WrapHandler(web.RequestHandler):
    def post(self):
        text = self.get_argument('text')
        width = self.get_argument('width', 40)
        self.write(textwrap.fill(text, int(width)))


if __name__ == '__main__':
    options.parse_command_line()
    app = web.Application(
        handlers=[
            (r'/reverse/(\w+)', ReverseHandler),
            (r'/wrap', WrapHandler)
        ]
    )
    http_server = httpserver.HTTPServer(app)
    http_server.listen(options.options.port)
    ioloop.IOLoop.instance().start()
