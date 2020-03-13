#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from pickle import dumps
from pickle import loads

from redis import ConnectionPool
from redis import StrictRedis


class RedisUtil:


    def __init__(self, host="127.0.0.1", port=6379, password=""):
        # decode_responses：默认False-返回bytes，True-返回string
        # 不过貌似没有用，python3查询返回的类型还是bytes
        self.redis = StrictRedis(connection_pool=ConnectionPool(host=host, port=port, password=password), decode_responses=True)


    def keys(self, key):
        data = self.redis.keys(key)
        if data is None:
            return None
        return data


    def set(self, key, value):
        self.redis.set(key, dumps(value))


    def get(self, key):
        data = self.redis.get(key)
        if data is None:
            return None
        return loads(data)


    def hset(self, name, key, value):
        self.redis.hset(name, key, dumps(value))


    def hget(self, name, key):
        data = self.redis.hget(name, key)
        if data is None:
            return None
        return loads(data)
