#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import platform
import sys
import pymongo
import time
from apps import redisapp


class MongoApp(object):
    def __init__(self,mongourl='localhost',port=27017):
        '''
        自动连接到mongo
        :param mongourl:
        :param port:
        '''
        self.url = mongourl
        self.port=port
        self.client = pymongo.MongoClient(self.url,self.port)

    def change_to_collection(self,coll,db='H5LSK'):
        '''
        切换到集合
        :param coll: 集合名称
        :param db: 数据库名称
        :return:
        '''
        self.collection = self.client[db][coll]

    def change_to_bd(self,c_db='H5LSK'):
        '''
        切换到数据库
        :param c_db:数据库名称
        :return:
        '''
        self.db = self.client[c_db]

    def choose_to_li(self,last_time,now_time):
        '''
        查询某时间段的数据
        :return:
        '''
        li=[]
        try:
            #res=self.collection.find({'$and':[{"time":{'$gt':"2019-06-11 09:21:27"}},{"time":{'$lte':"2019-06-13 09:23:23"}}]})
            res = self.collection.find({'$and': [{"time": {'$gt': last_time}}, {"time": {'$lte': now_time}}]})
        except Exception:
            print('please choose the databases ro collentions !')
        for i in res:
            try:
                if not i['isTry']:
                   li.append(i)
            except Exception as err:
                print (err)
        return li

    def mongoclose(self):
        '''
        关闭连接
        :return:
        '''
        self.client.close()

if __name__ == '__main__':
    if platform.system() == "Windows":
        BASE_DIR = '\\'.join(os.path.abspath(os.path.dirname(__file__)).split('\\')[:-1])  # for windos
        # print (BASE_DIR)
    else:
        BASE_DIR = '/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-1])  # for linux
    sys.path.append(BASE_DIR)

    mymongo = MongoApp()
    mymongo.change_to_collection('gameDetail')
    with open('time.log', 'r') as f:
        last_time = f.read().strip()
    now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open('time.log','w') as f:
        f.write(now_time)
    li=mymongo.choose_to_li(last_time,now_time)
    myredis = redisapp.RedisApp(li)
    mymongo.mongoclose()
    myredis.put_in_redis()  #记录数据录入redis
    myredis.get_record()    #根据记录增加用户金币，最后更新记录
    myredis.close_reids()
