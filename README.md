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



