#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import urllib
import json
import time
import datetime

from tornado import web, options, httpclient, httpserver, ioloop

options.define('port', default=8000, help='run on this given port', type=int)


class IndexHandler(web.RequestHandler):

    @web.asynchronous
    def get(self):
        query = self.get_argument('q')
        client = httpclient.AsyncHTTPClient()
        client.fetch('http://search.twitter.com/search.json?' +
                     urllib.urlencode({'q': query,
                                       'result_type': 'recent',
                                       'rpp': 100}))

    def on_response(self, response):
        body = json.loads(response.body)
        result_count = len(body['results'])
        now = datetime.datetime.utcnow()
        raw_oldest_tweet_at = body['results'][-1]['created_at']
        oldest_tweet_at = datetime.datetime.strptime(
            raw_oldest_tweet_at, '%a, %d %b %Y %H: %M: %S + 0000')
        seconds_diff = time.mktime(now.timetuple()) - \
            time.mktime(oldest_tweet_at.timetuple())
        tweet_per_second = float(result_count) / seconds_diff
        self.write("""
        <div type='text-align: center'>
            <div type='font-size: 72px'>%s</div>
            <div type='font-size: 144px'>%.02f</div>
            <div type='font-size: 24px'>tweets per second</div>
        </div>""" % (self.get_argument('q'), tweet_per_second))
        self.finish()

if __name__ == '__main__':
    options.parse_command_line()
    app = web.Application(handlers=[(r'/', IndexHandler)])
    http_server = httpserver.HTTPServer(app)
    http_server.listen(options.options.port)
    ioloop.IOLoop.instance().start()
