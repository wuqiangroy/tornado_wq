#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import os
import random

from tornado import httpserver, options, ioloop, web

options.define('port', default=8000, help='run this given port', type=int)


class IndexHandler(web.RequestHandler):

    def get(self):
        self.render('main_index.html')


class MungedPageHandler(web.RequestHandler):

    def map_by_first_letter(self, text):
        mapped = dict()
        for line in text.split('\r\n'):
            for word in [x for x in line.split(' ') if len(x) > 0]:
                if word[0] not in mapped:
                    mapped[word[0]] = []
                mapped[word[0]].append(word)
        return mapped

    def post(self):
        source_text = self.get_argument('source')
        text_to_change = self.get_argument('change')
        source_map = self.map_by_first_letter(source_text)
        change_lines = text_to_change.split('\r\n')
        self.render('munged.html', source_map=source_map,
                    change_lines=change_lines, choice=random.choice)


if __name__ == '__main__':
    options.parse_command_line()
    app = web.Application(
        handlers=[(r'/', IndexHandler),
                  (r'/poem', MungedPageHandler)],
        template_path=os.path.join(os.path.dirname(__file__), 'templates'),
        static_path=os.path.join(os.path.dirname(__file__), 'static'),
        debug=True
    )
    http_server = httpserver.HTTPServer(app)
    http_server.listen(options.options.port)
    ioloop.IOLoop.instance().start()


