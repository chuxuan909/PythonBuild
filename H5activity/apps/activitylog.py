#!/usr/bin/env python
# -*- coding:utf-8 -*-
import logging

class H5Log(object):
    def __init__(self):
        '''
        默认配置一个根logger控制器
        '''
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter(
            '%(asctime)s --- %(levelname)s: --- %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')

    def create_file_out(self):
        '''
        创建输出到文件的handler
        :return:
        '''
        self.fh = logging.FileHandler('log/h5activity.log')
        self.fh.setLevel(logging.DEBUG)
        self.fh.setFormatter(self.formatter)
        self.logger.addHandler(self.fh)

    def create_stream_out(self):
        '''
        创建输出到屏幕的handler
        :return:
        '''
        self.ch = logging.StreamHandler()
        self.ch.setLevel(logging.DEBUG)
        self.ch.setFormatter(self.formatter)
        self.logger.addHandler(self.ch)


    def out_info_log(self,message):
        try:
            self.logger.info(message)
        except Exception:
            print('you shoud create file of sream handler')



if __name__=='__main__':
    h5 = H5Log()
    h5.create_file_out()
    h5.create_stream_out()
    h5.out_info_log('test output infomation')




