#!/usr/bin/env python
import redis
from apps.activitylog import H5Log
from apps import redis_to_gold

class RedisApp(object):
    def __init__(self,lis):
        self.lis = lis
        #self.pool = redis.ConnectionPool('localhost',6379,db=6) #if your >= python 3.x
        self.pool = redis.ConnectionPool(host='localhost',port=6379,db=6,decode_responses=True) #for python 2.7
        self.connect = redis.Redis(connection_pool=self.pool)
        self.h5log = H5Log()
        self.h5log.create_stream_out()
        self.h5log.create_file_out()
        self.h5log.out_info_log('redis connect successfull')

    def put_in_redis(self):
        for i in self.lis:
            self.init_redis_value(i['uid'])
            if i['bingo'] == 0:
                self.incre_redis_value(str(i['uid']),'unbingo')
            else:
                self.incre_redis_value(str(i['uid']), 'bingo')
    def init_redis_value(self,uid):
        if not self.connect.exists(uid):
            self.connect.hmset(uid,{'unbingo':0,'bingo':0})
            self.h5log.out_info_log('new user create ! id is %s' % uid)

    def incre_redis_value(self,uid,indenti):
        self.connect.hincrby(uid,indenti,1)
        self.h5log.out_info_log('user\'s who id is  %s identifiy %s is +1' % (uid,indenti))

    def get_record(self):
        for i in self.connect.scan_iter():
            self.count_plus_gold(i)

    def count_plus_gold(self,uid):
        num_bingo=int(self.connect.hget(uid,'bingo'))
        num_unbingo=int(self.connect.hget(uid,'unbingo'))
        bingo_value,bingo_remainder = computation_for_redis(num_bingo)
        unbingo_value,unbingo_remainder = computation_for_redis(num_unbingo)
        sum_plus_gold = bingo_value*10+unbingo_value*20
        self.h5log.out_info_log('user id %s  will plus gold  %d ' % (uid,sum_plus_gold))
        self.h5log.out_info_log('user id %s  bingo count change to  %d ' % (uid,bingo_remainder))
        self.h5log.out_info_log('user id %s  unbingo count change to  %d ' % (uid,unbingo_remainder))
        #change user gold
        redis_to_gold.RedisGold().change_gold_value(uid,sum_plus_gold)
        self.h5log.out_info_log('user id %s  gold change is compeleted' % uid)
        #change user record
        self.update_user_record(uid,'bingo',bingo_remainder)
        self.update_user_record(uid,'unbingo',unbingo_remainder)

    def update_user_record(self,uid,key,num):
        self.connect.hset(uid,key,num)
        self.h5log.out_info_log('user id %s  %s count change in redis is compeleted  now is %d' % (uid,key,num))

    def close_reids(self):
        self.connect.connection_pool.disconnect()

def computation_for_redis(num,N=5):
    try:
        value=num//N
        remainder=num%N
        return (value, remainder)
    except TypeError:
        print('please guarantee your parameter type is int ')
