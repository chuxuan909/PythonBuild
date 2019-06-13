#!/usr/bin/env python
import redis

class RedisGold(object):
    def __init__(self):
        self.pool = redis.ConnectionPool(host='localhost',port=6379,db=5,decode_responses=True)
        self.connect = redis.Redis(connection_pool=self.pool)


    def change_gold_value(self,uid,num):
        self.init_key(uid)
        self.connect.hincrby('h5lskUserGold',uid,num)
        self.connect.connection_pool.disconnect()

    def init_key(self,uid):
        if not self.connect.exists('h5lskUserGold'):
            self.connect.hset('h5lskUserGold','demo',0)
        if not self.connect.hexists('h5lskUserGold',uid):
            self.connect.hset('h5lskUserGold',uid,0)
