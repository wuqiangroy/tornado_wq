#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import os

from tornado import httpserver, options, ioloop, web

options.define('port', default=7000, help='run this given port', type=int)


class IndexHandler(web.RequestHandler):

    def get(self):
        self.render('index.html')


class PoemPageHandler(web.RequestHandler):

    def post(self):
        noun1 = self.get_argument('noun1')
        noun2 = self.get_argument('noun2')
        verb = self.get_argument('verb')
        noun3 = self.get_argument('noun3')
        self.render('poem.html', roads=noun1, wood=noun2, made=verb,
                    difference=noun3)

if __name__ == '__main__':
    options.parse_command_line()
    app = web.Application(
        handlers=[(r'/', IndexHandler),
                  (r'/poem', PoemPageHandler)],
        template_path=os.path.join(os.path.dirname(__file__), 'templates'))
    http_server = httpserver.HTTPServer(app)
    http_server.listen(options.options.port)
    ioloop.IOLoop.instance().start()
