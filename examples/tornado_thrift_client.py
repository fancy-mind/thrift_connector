# -*- coding: utf-8 -*-
from __future__ import print_function
from tornado import gen

from tornado.ioloop import IOLoop

from pingpong_app.pingpong_sdk_tornado.pingpong import PingService
from thrift_connector.tornado import TornadoClientPool, TornadoThriftClient

pool = TornadoClientPool(
    PingService,
    'localhost',
    8880,
    connection_class=TornadoThriftClient
)


def callback(future):
    print(future.result())
    IOLoop.current().stop()


@gen.coroutine
def main():
    print("Sending Ping...")
    print("Receive:", (yield pool.ping()))
    print("Sleeping...")
    with (yield pool.connection_ctx()) as conn:
        yield conn.sleep(1)
    print("Waked!")
    print("Winning the match...")
    print("Receive:")
    pool.win().add_done_callback(callback)


IOLoop.current().add_callback(main)
IOLoop.current().start()
