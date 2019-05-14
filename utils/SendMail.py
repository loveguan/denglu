#!/usr/bin/env python

# encoding: utf-8

'''

@author: JOJ

@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.

@contact: zhouguanjie@qq.com

@software: JOJ

@file: SendMail.py

@time: 2019-05-10 8:20

@desc:

'''

from django.conf import  settings

def send_email(email, code):

    from django.core.mail import EmailMultiAlternatives

    subject = '来自www.liujiangblog.com的注册确认邮件'

    text_content = '''感谢注册www.test.com，这里是joj的博客和教程站点，专注于Python、Django和机器学习技术的分享！\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                    <p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>www.liujiangblog.com</a>，\
                    这里是joj的博客和教程站点，专注于Python、Django和机器学习技术的分享！</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()