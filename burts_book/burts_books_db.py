#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import os
import pymongo
from tornado import httpserver, ioloop, options, web, locale

options.define('port', default=8000, help='run on the given port', type=int)


class Application(web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r'/recommended/', RecommendedHandler),
        ]
        setting = dict(
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            ui_modules={'Book': BookModule},
            debug=True
        )
        conn = pymongo.MongoClient('localhost', 27017)
        self.db = conn.boolstore
        web.Application.__init__(self, handlers, **setting)


class MainHandler(web.RequestHandler):
    def get(self):
        self.render('book_index.html',
                    page_title="Burt's Books | Home",
                    header_text="Welcome to Burt's Books!"
                    )


class RecommendedHandler(web.RequestHandler):
    def get(self):
        coll = self.application.db.book
        books = coll.find()
        self.render(
            'recommended.html',
            page_title="Burt's Books | Recommended Reading",
            header_text="Recommended Reading",
            books=books
        )


class BookModule(web.UIModule):
    def render(self, book):
        return self.render_string(
            "Modules/books.html",
            book=book
        )

    def css_files(self):
        return '/static/js/recommended.css'

    def javascript_files(self):
        return '/static/js/recommended.js'


if __name__ == '__main__':
    options.parse_command_line()
    http_server = httpserver.HTTPServer(Application())
    http_server.listen(options.options.port)
    ioloop.IOLoop.instance().start()
