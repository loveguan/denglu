#!/usr/bin/env python

# encoding: utf-8

'''

@author: JOJ

@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.

@contact: zhouguanjie@qq.com

@software: JOJ

@file: message.py

@time: 2019-05-13 13:38

@desc:

'''

import smtplib
from email.mime.text import MIMEText
from email.utils import  formataddr

def email(email_list,content,subject="用户管理系统-用户注册"):

    msg=MIMEText(content,'plain','utf-8')
    msg['From']=formataddr(["用户管理系统",'zhouguanjie2005@163.com'])
    msg['Subject']=subject
    #smtp设置
    server = smtplib.SMTP("smtp.163.com", 25)
    server.login("zhouguanjie2005@163.com", "zhou789099")
    server.sendmail('zhouguanjie2005@163.com', email_list, msg.as_string())
    server.quit()
# email(['zhouguanjie@qq.com', ], 'xiaohuzuishuai')