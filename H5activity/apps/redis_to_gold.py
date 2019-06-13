#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
因为此模块是对redis真实的写操作
所以将它从redisapp中单独分离了出来
'''
import redis

class RedisGold(object):
    def __init__(self):
        '''
        1.自动连接redis 的gold db
        2.使用自定义日志输出模块
        :param lis: 接收查询到的列表数据
        '''
        self.pool = redis.ConnectionPool(host='localhost',port=6379,db=5,decode_responses=True) #最后的decode_responses选项参数在python 2.x中需要添加
        self.connect = redis.Redis(connection_pool=self.pool)


    def change_gold_value(self,uid,num):
        '''
        更新用户记录
        :param uid: redis hash name
        :param num_bingo: redis key value
        :param num_unbingo: redis key value
        :return:
        '''
        self.init_key(uid)
        self.connect.hincrby('h5lskUserGold',uid,num)
        self.connect.connection_pool.disconnect()

    def init_key(self,uid):
        '''
        如果redis的name和key不存在，则创建
        :param uid:
        :return:
        '''
        if not self.connect.exists('h5lskUserGold'):
            self.connect.hset('h5lskUserGold','demo',0)
        if not self.connect.hexists('h5lskUserGold',uid):
            self.connect.hset('h5lskUserGold',uid,0)



