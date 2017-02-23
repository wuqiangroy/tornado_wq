#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import json
import urllib
import datetime
import time
from tornado import httpserver, ioloop, options, web, httpclient

options.define('port', default=8000, help='run this given port', type=int)


class IndexHandler(web.RequestHandler):
    def get(self):
        query = self.get_argument('q')
        client = httpclient.HTTPClient()
        response = client.fetch('http://search.twitter.com/search.json?' +
                                urllib.urlencode({'q': query,
                                                  'result_type': 'recent',
                                                  'rpp': 100}))
        body = json.loads(response.body)
        result_count = len(body['results'])
        now = datetime.datetime.utcnow()
        raw_oldest_tweet_at = body['result'][-1]['created_at']
        oldest_tweet_at = datetime.datetime.striptime(
            raw_oldest_tweet_at, '%a %d %b %Y %H:%M:%S + 0000')
        seconds_diff = time.mktime(now.timetuple()) - \
            time.mktime(oldest_tweet_at.timetuple())
        tweet_per_second = float(result_count) / seconds_diff
        self.write("""
        <div style='text-align: center'>
            <div style='font-size: 72px'>%s</div>
            <div style='font-size: 144px'>%0.2f</div>
            <div style='font-size: 24px'>tweets per second</div>
        </div>""" % (query, tweet_per_second))

if __name__ == '__main__':
    options.parse_command_line()
    app = web.Application(handlers=[
        (r'/', IndexHandler)])
    http_server = httpserver.HTTPServer(app)
    http_server.listen(options.options.port)
    ioloop.IOLoop.instance().start()



