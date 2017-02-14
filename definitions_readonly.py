#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import pymongo
from tornado import httpserver, options, web, ioloop

options.define('port', default=8000, help='run on the given port', type=int)


class Application(web.Application):
    def __init__(self):
        handlers = [(r'/(\w+)', WordHandler)]
        conn = pymongo.MongoClient('localhost', 27017)
        self.db = conn['example']
        web.Application.__init__(self, handlers, debug=True)


class WordHandler(web.RequestHandler):
    def get(self, word):
        coll = self.application.db.words
        word_doc = coll.find_one({'word': word})
        if word_doc:
            del word_doc['_id']
            self.write(word_doc)
        else:
            self.set_status(404)
            self.write({'error': 'word not found'})


if __name__ == '__main__':
    options.parse_command_line()
    http_server = httpserver.HTTPServer(Application())
    http_server.listen(options.options.port)
    ioloop.IOLoop.instance().start()
