#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Python2.x除法保留2位小数
# from __future__ import division
# from __future__ import print_function
# from __future__ import unicode_literals


from sqlalchemy import Column,create_engine,Integer,DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import and_
from sqlalchemy import inspect
import argparse,sys
import datetime

#Python2.x的中文支持
# reload(sys)
# sys.setdefaultencoding('utf-8')

#用户全局变量
stables_count=511
engine01 = create_engine('mysql+pymysql://mysqluser:mysqlpassword@mysqlserverip:3306/db0', max_overflow=15, echo=False)
engine02 = create_engine('mysql+pymysql://root:sEqGH0W1SivoYDIRTuul@mysqlserverip:3306/db1', max_overflow=15, echo=False)
Satisfy_reg_uidset=[]
Satisfy_login_set=[]

base=declarative_base()
##获取数据库内所有表的信息#######
# base.metadata.reflect(engine01)
# tables = base.metadata.tables
# print(tables)
##获取数据库内所有表的信息 END####

def usage():
    '''
    输出帮助信息
    '''
    print(
"""
Usage:  sys.args[0]       [option] 

[option]：

-h or --help：显示帮助信息
-l or --login：指定查询那个日期的登录记录      例如: 2019-06-06
-r or --reg：指定查询那个日期的注册记录      例如: 2019-06-06
"""
    )

def argv_check():
    '''
    判断是否输入了参数
    '''
    if len(sys.argv) == 1:
        usage()
        sys.exit()

def parser_flag():
    '''
    获取用户输入参数的函数
    :return:
    '''
    #帮助信息
    parser=argparse.ArgumentParser(description="输入登录记录和注册记录的查询日期")
    #相关选项
    parser.add_argument("-l","--login",help="指定查询那个日期的登录记录      例如: 2019-06-06")
    parser.add_argument("-r","--reg",help="指定查询那个日期的注册记录      例如: 2019-06-06")
    #获取参数
    # args=parser.parse_args()
    return parser.parse_args()

def date_oper(srt_time):
    '''
    日期处理
    :param srt_time:
    :return: 返回当前日期后一天的日期
    '''
    try:
        now=datetime.datetime.strptime(srt_time,'%Y-%m-%d')
        now_later=now+datetime.timedelta(days=1)
        return  now_later.strftime('%Y-%m-%d')
    except ValueError:
        print("请输入正确的日期格式")
        sys.exit(600)

def Satisfy_db(engine,reg_time,login_time):
    '''
    使用检测器循环的取出数据库内的每一张表
    '''
    SessionCls = sessionmaker(bind=engine)
    session = SessionCls()

    inspector = inspect(engine)
    print('platSvrUserInfo库%s引擎查询中，请稍候...' % engine)
    for table_name in inspector.get_table_names():
        query_db(table_name,session,reg_time,login_time)

def query_db(table_name,session,reg_time,login_time):
    '''
    查询表内的数据
    使用条件查询满足条件的记录并放入列表
    '''
    ##日期处理##
    reg_time_later=date_oper(reg_time)
    login_time_later=date_oper(login_time)
    class userInfo(base):
        __tablename__ = table_name
        uid = Column(Integer, primary_key=True, autoincrement=True)
        loginTime = Column(DateTime)
        registerTime = Column(DateTime)
    reg_objs=session.query(userInfo).filter(and_(userInfo.registerTime>= reg_time ,userInfo.registerTime < reg_time_later ))
    login_objs=session.query(userInfo).filter(and_(userInfo.loginTime>= login_time ,userInfo.loginTime < login_time_later))
    try:
        for index_obj in reg_objs:
            Satisfy_reg_uidset.append(index_obj.uid)
        for index in login_objs:
            Satisfy_login_set.append(index.uid)
    except AttributeError:
        print('查询的值不存在')

if __name__ == '__main__':
    argv_check()
    args = parser_flag()

    Satisfy_db(engine01, args.reg, args.login)
    Satisfy_db(engine02, args.reg, args.login)
    Satisfy_reg_uidset = set(Satisfy_reg_uidset)
    # print(Satisfy_reg_uidset)
    print('%s 总计注册了%d人' % (args.reg,len(Satisfy_reg_uidset)))

    Satisfy_login_set = set(Satisfy_login_set)
    print('%s 总计登录了%d人' % (args.login,len(Satisfy_login_set)))

    #2个集合取交集，得到规定时间内即注册又登录的用户
    Inter_set=Satisfy_reg_uidset.intersection(Satisfy_login_set)
    print("在%s登录，并在%s注册过的人有：%d人" % (args.login,args.reg,len(Inter_set)))

    print("在%s登录，并在%s注册的留存率：%0.2f%%" % (args.login,args.reg,(len(Inter_set)/len(Satisfy_reg_uidset)*100)))