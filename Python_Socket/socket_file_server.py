#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
使用socket传送文件
服务端代码
"""
import socketserver
import struct

ipaddr=('192.168.0.210',9339)
FILE_PATH='e:\\b.mkv'
FILE_PATH2='e:\\'
class MYhandle(socketserver.BaseRequestHandler):
    def handle(self):
        cli_data=self.request.recv(1024)
        filename,file_size = struct.unpack('128sl',cli_data)
        filename=str(filename.decode())
        self.request.sendall(bytes('302','utf8'))
        print(filename)
#        f=open(filename,'wb')
        f=open(FILE_PATH,'wb')
#       f=open('E:\\b.jpg','wb')
        rev_data=0
        while rev_data != file_size:
            c_data=self.request.recv(1024)
            rev_data+=len(c_data)
            f.write(c_data)
        f.close()

server=socketserver.ThreadingTCPServer(ipaddr,MYhandle)

print('waiting for connecting... ...')
server.serve_forever()


