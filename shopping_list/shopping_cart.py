#!/usr/bin/env python
# _*_ coding:utf-8 _*_

# 长轮询

from uuid import uuid4
from tornado import web, options, httpserver, ioloop

options.define('port', default=8000, help='run on this given port', type=int)


class ShoppingCart(object):

    TotalInventory = 10
    callbacks = []
    carts = {}

    def register(self, callback):
        self.callbacks.append(callback)

    def move_item_to_cart(self, session):
        if session in self.carts:
            return

        self.carts[session] = True
        self.notify_callbacks()

    def remove_item_to_cart(self, session):
        if session not in self.carts:
            return

        del(self.carts[session])
        self.notify_callbacks()

    def notify_callbacks(self):
        for c in self.callbacks:
            self.call_back_helper(c)

        self.callbacks = []

    def call_back_helper(self, callback):
        callback(self.get_inventory_count())

    def get_inventory_count(self):
        return self.TotalInventory - len(self.carts)


class DetailHandler(web.RequestHandler):

    def get(self):
        session = uuid4()
        count = self.application.ShoppingCart.get_inventory_count()
        self.render('index.html', session=session, count=count)


class CartHandler(web.RequestHandler):

    def post(self):
        action = self.get_argument('action')
        session = self.get_argument('session')

        if not session:
            self.set_status(400)
            return

        if action == 'add':
            self.application.ShoppingCart.move_item_to_cart(session)
        elif action == 'remove':
            self.application.ShoppingCart.remove_item_to_cart(session)
        else:
            self.set_status(400)


class StatusHandler(web.RequestHandler):

    @web.asynchronous
    def get(self):
        self.application.ShoppingCart.register(
            self.async_callback(self.on_message))

    def on_message(self, count):
        self.write("{'InventoryCount': '%d'}" % count)
        self.finish()


class Application(web.Application):
    def __init__(self):
        self.ShoppingCart = ShoppingCart()

        handlers = [
            (r'/', DetailHandler),
            (r'/cart', CartHandler),
            (r'/cart/status', StatusHandler),
        ]

        setting = {
            'template_path': 'templates',
            'static_path': 'static'
        }

        web.Application.__init__(self, handlers, **setting)

if __name__ == '__main__':
    options.parse_command_line()
    app = Application()
    server = httpserver.HTTPServer(app)
    server.listen(8000)
    ioloop.IOLoop.instance().start()

