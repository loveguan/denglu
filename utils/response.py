#!/usr/bin/env python

# encoding: utf-8

'''

@author: JOJ

@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.

@contact: zhouguanjie@qq.com

@software: JOJ

@file: response.py

@time: 2019-05-13 9:27

@desc:

'''

class StatusCodeEnum:

    Failed = 1000
    AuthFailed = 1001
    ArgsError = 1002

    Success = 2000
    # 发帖

    # 评论

    # 点赞
    FavorPlus = 2301
    FavorMinus = 2302


class BaseResponse:

    def __init__(self):
        self.status = False
        self.code = StatusCodeEnum.Success
        self.data = None
        self.summary = None
        self.message = {}