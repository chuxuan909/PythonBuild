#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
socket传输文件代码
客户端
"""
import  socket
import os
import struct

FILE_PATH='f:\\b.mkv'

ipaddr=('192.168.0.210',9339)
cm=socket.socket()
cm.connect(ipaddr)

file_name=os.path.basename(FILE_PATH)
file_size=os.stat(FILE_PATH).st_size
file_name=bytes(file_name,'utf8')
fhead=struct.pack('128sl',file_name,file_size)
cm.send(fhead)
tmpdata=cm.recv(1024)

f=open(FILE_PATH,'rb')
while True:
    filedata = f.read(1024)
    if not filedata: break
    cm.send(filedata)
f.close()
