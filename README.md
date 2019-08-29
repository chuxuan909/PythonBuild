# PythonBuild
There are thing projects or scripts developed by python

**各种目录和目录简介**

## Python_Script

备份平时写的一些脚本代码，目的在于使用其他脚本时，可以从备份的脚本内拷贝一些常用的方法或函数

## Python_for_wechat

python调用微信的消息通知API的脚本，执行该脚本可以实现自动将信息发送给企业微信指定的组员。注意脚本代码中的类里的 ```def sendMessage(self,message)```
方法接收的参数就是你想要发送的信息，类型为字符串

具体使用案例，参考：https://www.yuque.com/ppsha/deploy/qpkeip

## H5activity

通过对mongodb和redis的操作来对H5游戏的金币数据进行修改的一个小项目。该项目作为H5游戏的一个“小活动”而被发布。主要流程有：

- 滚动从mongodb获取某个时间段的数据
- 将获取到的数据存入redis
- 操作数据，记录更新

整个项目对数据库的操作居多，剩余的就是logging日志模块相关操作

## Python_for_Zabbix

Python对zabbix的api的使用。利用zabbix的api我们可以直接使用python进行zabbix的各个对象的管理。比如 监控项、触发器等

目前此项目只实现的功能有：

- 添加监控项

zabbix api的文档，参考：https://www.zabbix.com/documentation/3.4/zh/manual/api

> zabbix3.4版本以下为英文文档，参考：https://www.zabbix.com/documentation/3.0/manual/api

## H5uerate

使用sqlalchemy对MySQL数据库进行统计，计算出用户的留存率的小项目。

留存率举例讲解：

假设2019-06-06日期注册用户有 1000 个

假设2019-06-06日期注册用户并在2019-06-07又登录的用户有 400 个

那么2019-06-06日期注册用户在2019-06-07留存率为： 400/1000 * 100 = 40%

## Python_svn

使用python进行SVN的checkout操作

- 1.拉取出项目代码到本地，并压缩
- 2.使用ansible将拉取的项目代码再部署到服务器上面去

