#!/usr/bin/env python
# encoding=utf-8

import redis


class Redis(object):
    def __init__(self, host, port, auth=None):
        self._host = host
        self._port = port
        self._auth = auth
        rdp = redis.ConnectionPool(host=host, port=port, socket_timeout=60, socket_connect_timeout=5, max_connections=2)
        self._con = redis.Redis(connection_pool=rdp)

        if auth:
            try:
                self._con.execute_command('auth', auth)
            except Exception as e:
                print(e)

    def reconnect(self):
        rdp = redis.ConnectionPool(host=self._host, port=self._port, socket_timeout=60, socket_connect_timeout=5,
                                   max_connections=2)
        self._con = redis.Redis(connection_pool=rdp)

        if self._auth:
            try:
                self._con.execute_command('auth', self._auth)
            except Exception as e:
                print(e)

    def get(self, count):
        try:
            items = self._con.mget(count)
            return items
        except Exception as e:
            print(1111, e)
            self.reconnect()

    def set(self, key, value):
        try:
            return self._con.set(key, value)
        except redis.TimeoutError as rc_error:
            print(rc_error)
            self.reconnect()
        except Exception as e:
            print(e)
            self.reconnect()


if __name__ == "__main__":
    import time
    import json
    rc = Redis(host='uat-shylf-databus.bilibili.co',
               port=6205,
               auth='0e3f30683b9a83d9:'
                    '9d1250ee4970455c3f66b97947d2f42e@'
                    'RangoJob-Uat-TestEp-P/topic=RangoJob-Uat-T&role=pub'
               )
    print(rc.set(1, '{"name": 2, "age": 2}'))

    sub_rc = Redis(host='uat-shylf-databus.bilibili.co',
                   port=6205,
                   auth='0e3f30683b9a83d9:'
                        '9d1250ee4970455c3f66b97947d2f42e@'
                        'RangoJob-Uat-TestEp-S/topic=RangoJob-Uat-T&role=sub'
                   )

    while True:
        items = sub_rc.get(1000)
        print(items)
        # continue
        if not items:
            continue
        else:
            for item in items:
                ret = json.loads(item)
                print(ret)
                sub_rc.set(ret['partition'], ret['offset'])
