#!/usr/bin/env python
import logging

class H5Log(object):
    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter(
            '%(asctime)s --- %(levelname)s:%(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')

    def create_file_out(self):
        self.fh = logging.FileHandler('log/h5activity.log')
        self.fh.setLevel(logging.DEBUG)
        self.fh.setFormatter(self.formatter)
        self.logger.addHandler(self.fh)

    def create_stream_out(self):
        self.ch = logging.StreamHandler()
        self.ch.setLevel(logging.DEBUG)
        self.ch.setFormatter(self.formatter)
        self.logger.addHandler(self.ch)


    def out_info_log(self,message):
        try:
            self.logger.info(message)
        except Exception:
            print('you shoud create file of sream handler')
