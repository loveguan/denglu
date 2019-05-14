#!/usr/bin/env python

# encoding: utf-8

'''

@author: JOJ

@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.

@contact: zhouguanjie@qq.com

@software: JOJ

@file: forms.py

@time: 2019-05-09 15:38

@desc:

'''
from django import forms

class UserForom(forms.Form):
    username=forms.CharField(label='用户名',max_length=128)
    password=forms.CharField(label='密码',max_length=256)
    chkcode = forms.CharField(label='验证码',max_length=10)

class RegisterForm(forms.Form):
    gender=(
        ('mail',"男"),
        ('femail',"女")
    )
    username=forms.CharField(label="用户名",max_length=128,widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256,widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=gender)
    chkcode = forms.CharField(label='验证码', max_length=10)

class SendMsgForm(forms.Form):
    email=forms.EmailField()
