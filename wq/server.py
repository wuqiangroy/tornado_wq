#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from tornado import ioloop, options, httpserver
from application import application

options.define('port', default=8000, help='run on this given port', type=int)


def main():
    options.parse_command_line()
    http_server = httpserver.HTTPServer(application)
    http_server.listen(options.options.port)

    print("Development server is running at http://127.0.0.1:%s"
          % options.options.port)
    print("Quit the server with CTRL-C")

    ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
