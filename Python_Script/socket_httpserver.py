#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
使用socket实现http请求(伪静态web服务器)
"""


###############socketsever实现socket的http通信(多线程)#######################
import socketserver

ip_addr=('127.0.0.1',80)

class mysocket(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            data=self.request.recv(1024)
            print(data.decode())
            self.request.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
            with open('F:/PythonBuild/learn/les15/damon.html', 'rb') as f:
                 self.request.sendall(f.read())
            self.request.close()
        except ConnectionAbortedError:
            pass

socket1=socketserver.ThreadingTCPServer(ip_addr,mysocket)

socket1.serve_forever()
##########################################################################

####################socket简单实现http请求(单进程)#########################
# import socket
#
#
# def handle_request(client):
#     buf = client.recv(1024)
#     print(buf)
#     client.send(b"HTTP/1.1 200 OK\r\n\r\n")
#     client.send(b"<h1>Hello, World</h1>")
#
#
# def main():
#     sock = socket.socket()
#     sock.bind(('localhost', 80))
#     sock.listen(5)
#
#     while True:
#         connection, address = sock.accept()
#         handle_request(connection)
#         connection.close()
#
#
# if __name__ == '__main__':
#     main()
##########################################################################

# ###############使用协程异步实现socket通信###############################
# import socket
# import gevent  # 使用pip安装
# from gevent import socket, monkey
#
# monkey.patch_all()
#
#
# def server(port):
#     s = socket.socket()
#     s.bind(('0.0.0.0', port))
#     s.listen(500)
#     while True:
#         cli, addr = s.accept()
#         gevent.spawn(handle_request, cli)  # 至关重要的一句话，创建协程任务，执行函数为handle_request，并将socket客户端的操作实例传入
#
#
# def handle_request(conn):  # 此函数的参数是socket客户端的操作实例
#     try:
#         while True:
#             data = conn.recv(1024)
#             # 3.发送socket的http应答码
#             recv_data = b"HTTP/1.1 200 OK\r\n\r\n"  # 3.x版本需要发送格式为2进制格式
#             conn.send(recv_data)
#             # 4.开始发送字符串，即html代码到浏览器
#             with open('F:/PythonBuild/learn/les15/damon.html', 'rb') as f:  # 字符串，html代码从文件中读取,3.x版本需要发送格式为2进制格式
#                 conn.send(f.read())
#             if not data:
#                 conn.shutdown(socket.SHUT_WR)
#     except Exception:
#         pass
#     finally:
#         conn.close()
#
#
# if __name__ == '__main__':
#     server(80)
# ####################################
