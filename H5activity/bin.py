#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import platform
import sys
import time

from apps import mongoapp
from apps import redisapp

if platform.system() == "Windows":
    BASE_DIR = '\\'.join(os.path.abspath(os.path.dirname(__file__)).split('\\')[:-1]) #for windos
    #print (BASE_DIR)
else:
    BASE_DIR = '/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-1])  #for linux
sys.path.append(BASE_DIR)

def main():
    mymongo = mongoapp.MongoApp()
    mymongo.change_to_collection('gameDetail')
    with open('conf/time.conf', 'r') as f:
        last_time = f.read().strip()
    now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open('conf/time.conf','w') as f:
        f.write(now_time)
    li=mymongo.choose_to_li(last_time,now_time)
    myredis = redisapp.RedisApp(li)
    mymongo.mongoclose()
    myredis.put_in_redis()  
    myredis.get_record()   
    myredis.close_reids()

if __name__ == '__main__':
    main()
