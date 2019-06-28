#!/usr/bin/env python
# -*- coding:utf-8 -*-
## author: chenjie
##Version: V1.0.0
##Note: 利用zabbix的api来操作zabbix

import requests
import json

class zabbix(object):
    def __init__(self):
        '''
        连接到zabbix的api接口
        获取tocken
        '''
        #获取tocken的post请求中需要用到的参数
        self.url = 'http://zabbix.xxxx.cn/api_jsonrpc.php'  ###zabbix的api url
        self.headers = {'Content-Type': 'application/json'}
        auth = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": "your id",                     ###登陆用户名
                "password":"your password"    ###登陆密码
            },
            "id": 1,
            "auth":None,
        }
        # 发送post请求
        response = requests.post(self.url, data=json.dumps(auth), headers=self.headers)
        # 获取tocken
        self.tocken = json.loads(response.text)['result']

    def get_hosts(self):
        '''
        获取主机列表
        '''
        neirong = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": [
                    "hostid",
                    "host"
                ],
                "selectInterfaces": [
                    "interfaceid",
                    "ip"
                ]
            },
            "id": 2,
            "auth": self.tocken
        }
        response = requests.post(self.url, data=json.dumps(neirong), headers=self.headers)
        #注意:这里输出主机列表，然后记住你想操作的主机的interfaceid和hostid的值
        print(response.text)

    def get_templates(self,template_name):
        '''
        按照模板名获取模板列表
        '''
        neirong = {
            "jsonrpc": "2.0",
            "method": "template.get",
            "params": {
                "output": "extend",
                "filter": {
                    "host": [
                        template_name,
                    ]
                }
            },
            "auth": self.tocken,
            "id": 4
        }
        response = requests.post(self.url, data=json.dumps(neirong), headers=self.headers)
        # 注意:这里输出主机列表，然后记住你想操作的主机的interfaceid和hostid的值
        print(response.text)

    def host_item_add(self,host_id,host_interface_id,item_name,item_key,units="",delta=0):
        '''
        给选择的主机/模板添加监控项
        字符串:param host_id: 你想操作的 "主机的hostid值/模板的templateid值",使用 "get_host()/get_templates()" 方法查找
        字符串:param host_interface_id: 你想操作的主机的interfaceid值,使用get_host()方法查找,模板可以随便写
        字符串:param item_name: 监控项的名称
        字符串:param item_key: 监控项客户端的key名称
        :return:
        '''
        neirong ={
            "jsonrpc": "2.0",
            "method": "item.create",
            "params": {
                "name": item_name,
                "key_": item_key,
                "hostid": host_id,
                "interfaceid": host_interface_id,
                "type": 0,       #客户端类型，0表示zabbix_agent
                "value_type": 0, #获取的key的值类型，0是float类型
                "history": 3,    #数据保留时间,单位 天
                "trends": 7,     #图形趋势保留时间，单位 天
                "delay": 60,     #间隔多少秒采集一次
                "units": units,  #获取的key的值的单位
                "delta": delta,  #存储值，1表示每秒速率
            },
            "auth": self.tocken ,
            "id": 3
        }
        response = requests.post(self.url, data=json.dumps(neirong), headers=self.headers)
        print(response.text)

    def key_list(self,keyfile_path='./cproc.list'):
        '''
        批量添加监控项
        一个一个添加太麻烦，将需要添加的服务的监控key放在一个文件内
        然后读取文件里面的内容
        :param keyfile_path: key的列表文件
        :return:
        '''
        with open(keyfile_path,'r') as f:
            return [li.rstrip('\n') for li in f]

def main():
    zabbix_chen = zabbix()
    # zabbix_chen.get_hosts() #输出主机列表，记住你你想操作的主机的interfaceid和hostid的值
    # zabbix_chen.get_templates("node_servers_template")

    ## 添加监控项
    # zabbix_chen.host_item_add("10108","1","[Mongodb当前更新的操作数]","mongo.stat[update]")
    # zabbix_chen.host_item_add("10108","1","H5FishSvr_fishServer-server-1","node.server[21997,fishServer-server-1]")

    ## net_out和net_in
    #zabbix_chen.template_item_add("mongo_stat_template","10109","[Mongodb每秒更新操作数]","mongo.stat[update]","qbp")

    ## 批量添加监控项
    for index in zabbix_chen.key_list():
        zabbix_chen.host_item_add("10108", "1", "H5FishSvr_%s" % index,
                                  "node.server[21997,%s]" % index)

if __name__ == "__main__":
    main()






