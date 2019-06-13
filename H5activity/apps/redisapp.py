#!/usr/bin/env python
# -*- coding:utf-8 -*-
import redis

from apps import redis_to_gold
from apps.activitylog import H5Log  # 加载自定义日志输出模块


class RedisApp(object):
    def __init__(self,lis):
        '''
        1.自动连接redis
        2.使用自定义日志输出模块
        :param lis: 接收查询到的列表数据
        '''
        self.lis = lis
        self.pool = redis.ConnectionPool(host='localhost',port=6379,db=6,decode_responses=True) #最后的decode_responses选项参数在python 2.x中需要添加
        self.connect = redis.Redis(connection_pool=self.pool)
        #输出日志模式调整
        self.h5log = H5Log()
        self.h5log.create_stream_out()
        self.h5log.create_file_out()
        # 输出日志
        self.h5log.out_info_log('redis connect successfull')

    def put_in_redis(self):
        '''
        将指定列表内的数据存入reids
        :return:
        '''
        for i in self.lis:
            self.init_redis_value(i['uid'])
            if i['bingo'] == 0:
                self.incre_redis_value(i['uid'],'unbingo')
            else:
                self.incre_redis_value(i['uid'], 'bingo')

    def init_redis_value(self,uid):
        '''
        初始化新的用户uid
        :param uid: 用户uid
        :return:
        '''
        if not self.connect.exists(uid):
            self.connect.hmset(uid,{'unbingo':0,'bingo':0})
            self.h5log.out_info_log('new user create ! id is %s' % uid)

    def incre_redis_value(self,uid,indenti):
        '''
        用户redis内的信息更新(递增)
        :param uid:
        :param indenti:
        :return:
        '''
        self.connect.hincrby(uid,indenti,1)
        self.h5log.out_info_log('user\'s who id is  %s identifiy %s is +1' % (uid,indenti))

    def close_reids(self):
        '''
        关闭reids连接
        :return:
        '''

    def get_record(self):
        '''
        依次取出redis中的key
        并将key传给count_plus_gold方法
        :return:
        '''
        for i in self.connect.scan_iter():
            self.count_plus_gold(i)

    def count_plus_gold(self,uid):
        '''
        计算用户应该增加多少金币,以及增加后剩余的记录次数
        :param uid:
        :return:
        '''
        num_bingo=int(self.connect.hget(uid,'bingo'))
        num_unbingo=int(self.connect.hget(uid,'unbingo'))
        bingo_value,bingo_remainder = computation_for_redis(num_bingo)
        unbingo_value,unbingo_remainder = computation_for_redis(num_unbingo)
        sum_plus_gold = bingo_value*10+unbingo_value*20  #总计要增加多少金币
        self.h5log.out_info_log('user id %s  will plus gold  %d ' % (uid,sum_plus_gold))
        self.h5log.out_info_log('user id %s  bingo count change to  %d ' % (uid,bingo_remainder))
        self.h5log.out_info_log('user id %s  unbingo count change to  %d ' % (uid,unbingo_remainder))

        #更新用户金币记录
        redis_to_gold.RedisGold().change_gold_value(uid, sum_plus_gold)
        self.h5log.out_info_log('user id %s  gold change is compeleted' % uid)

        #更新用户记录
        self.update_user_record(uid,'bingo',bingo_remainder)
        self.update_user_record(uid,'unbingo',unbingo_remainder)

    def update_user_record(self,uid,key,num):
        '''
        更新用户记录
        :param uid: redis hash name
        :param num_bingo: redis key value
        :param num_unbingo: redis key value
        :return:
        '''
        self.connect.hset(uid,key,num)
        self.h5log.out_info_log('user id %s  %s count change in redis compelet now is %d' % (uid,key,num))



def computation_for_redis(num,N=5):
    '''
    取除法运算试的值和余数
    除数默认是5
    :param num:
    :return:
    '''
    try:
        value=num//N
        remainder=num%N
        return (value, remainder)
    except TypeError:
        print('please guarantee your parameter type is int ')



if __name__ == '__main__':
    import  os,sys,platform
    if platform.system() == "Windows":
        BASE_DIR = '\\'.join(os.path.abspath(os.path.dirname(__file__)).split('\\')[:-1])  # for windos
        # print (BASE_DIR)
    else:
        BASE_DIR = '/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-1])  # for linux
    sys.path.append(BASE_DIR)
