#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 从配置文件中读取svn代码地址
# 并且拉取代码
import pysvn
import sys, os
import shutil

reload(sys)
sys.setdefaultencoding('utf-8')

import locale

locale.setlocale(locale.LC_ALL, '')

# 变量
out_path = "/opt/ansible/projects"  # svn取出代码的目标根路径
svnurl_root = "svn://xx.xx.xx.xx/tags/release/backend"  # svn代码的根目录
config_file = "/opt/ansible/vars/main.yml"  # 配置文件位置
download_dir = "/opt/ansible/projects"


# SVN认证
def get_login(realm, username, may_save):
    retcode = False  # True，如果需要验证；否则用False
    username = 'server'  # 用户名
    password = 'xxxx'  # 密码
    save = False  # True，如果想之后都不用验证；否则用False
    return retcode, username, password, save


client = pysvn.Client()
client.callback_get_login = get_login


# 从SVN中check out出代码
def svn_checkout(svnurl, out_path):
    global svnurl_root
    client.checkout("%s/%s" % (svnurl_root, svnurl), out_path)  # 从SVN中取出最新版本
    # 从SVN中取出指定版本
    # rv = pysvn.Revision(pysvn.opt_revision_kind.number, 1111))
    # client.checkout(svnurl, outpath, revision=rv)               #取出指定版本1111
    # Revision类型可以通过rv.number获取对应的数字


# 开始读配置文件
os.chdir(download_dir)


with open(config_file, 'r') as f:
    for index in f:
        project_tags = index.strip().split(":")[1].strip()
        project_name = project_tags.split("_")[0].strip()
        svn_checkout(project_tags, "%s/Release_%s" % (out_path, project_name))  # 取出SVN代码,放在指定的目录下
        # shutil.make_archive("Release_%s" % project_name,'gztar',"Release_%s" % project_name) #python3.X
        try:
            os.remove("Release_%s.tar.gz" % project_name)
        except OSError:
            print("Release_%s.tar.gz 文件已经被删除或者根本不存在!" % project_name)
        os.system("tar -zcvf Release_%s.tar.gz Release_%s" % (project_name,project_name))
