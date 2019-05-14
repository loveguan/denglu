from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from app1 import models
from . import forms
from utils import check_code as CheckCode
from utils import SendMail
import io
from django.conf import settings
from utils import response
from utils.commons import random_code
import json
import datetime
from utils import message


# Create your views here.

def test(req):
    return HttpResponse('test')


def index(req):
    return render(req, 'login/index.html', locals())


def login(req):
    message = ''
    if req.method == 'POST':
        login_form = forms.UserForom(req.POST)
        if login_form.is_valid():
            # username = req.POST.get('username')
            # password = req.POST.get('password')
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            check_code = login_form.cleaned_data.get('chkcode')
            print(username, password, check_code)
            # 验证码校验
            if req.session["CheckCode"].lower() != check_code.lower():
                message = '验证码错误！！'
                return render(req, 'login/login.html', {'message': message})

            # 判断输入是否为空，判断用户名密码是否正确
            if username.strip() and password:
                from django.db.models import Q
                con = Q()
                con.connector = 'AND'
                con.children.append(('name', username))
                con.children.append(('password', password))
                obj = models.User.objects.filter(con).first()
                if obj:
                    print('login sucess')
                    req.session['is_login'] = True
                    req.session['user_id'] = obj.id
                    req.session['user_name'] = obj.name
                    # request.session['user_info'] = {'nid': obj.nid, 'email': obj.email, 'username': obj.username}
                    return redirect('/index/')
                else:
                    message = '用户名或者密码填写错误'
                    print('login error')
            else:
                print('1112error')
                message = '请检查输入的内容是否正确'
    # login_form=forms.UserForom()
    elif req.method == "GET":
        if req.session.get('is_login', None):
            print('eeee')
            return redirect("/index/")
    return render(req, 'login/login.html', {'message': message})


# 发送验证码
def send_msg(req):
    # 基本的回复，写在类中
    rep = response.BaseResponse()
    # 在forms.py有东西
    form = forms.SendMsgForm(req.POST)
    if form.is_valid():
        # _value_dict=form.clean()
        # email=_value_dict['email']
        email_list = []
        email = form.cleaned_data['email']
        has_exits_email = models.User.objects.filter(email=email)
        if has_exits_email:
            rep.summary = '此邮箱已经被注册！！！'
            print('已经存在！！！')
            return HttpResponse(json.dumps(rep.__dict__))
        email_list.append(email)
        # 当前时间
        current_date = datetime.datetime.now()
        # 生成随机码
        code = random_code()
        count = models.SendMsg.objects.filter(email=email).count()
        if not count:
            models.SendMsg.objects.create(code=code, email=email, ctime=current_date)
            rep.status = True
            message.email([email, ], code)
        else:
            limit_day = current_date - datetime.timedelta(hours=1)
            times = models.SendMsg.objects.filter(email=email, ctime__gt=limit_day, times__gt=9).count()
            if times:
                print('exceed max number')
                rep.summary = "'已超最大次数（1小时后重试！！！）'"
            else:
                unfreeza = models.SendMsg.objects.filter(email=email, ctime__lt=limit_day).count()
                if unfreeza:
                    models.SendMsg.objects.filter(email=email).update(times=0)
                from django.db.models import F
                models.SendMsg.objects.filter(email=email).update(code=code, ctime=current_date,
                                                                  times=F('times') + 1)
                rep.status = True
                message.email(email_list, code)
    else:
        error_msg = form.errors['email'][0]
        rep.summary = error_msg
        print('error')
        return HttpResponse(json.dumps(response.__dict__))

    return HttpResponse(json.dumps(rep.__dict__))


# 注册
def register(req):
    if req.session.get('is_login', None):
        return redirect('/index/')
    if req.method == 'POST':
        register_form = forms.RegisterForm(req.POST)
        message = "请检查填写的内容"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')
            chkcode = register_form.cleaned_data.get('chkcode')
            print(username, password1, password2, email, chkcode, sex)

            # 验证码校验，一分钟之内的
            current_date = datetime.datetime.now()
            limit_day = current_date - datetime.timedelta(minutes=1)
            is_valid_code = models.SendMsg.objects.filter(email=email, code=chkcode, ctime__gt=limit_day).count()
            if not is_valid_code:
                message = "输入的验证码不正确或者已经过期！！"
                return render(req, 'login/register.html', locals())
            if password1 != password2:
                message = "两次输入的密码不相同"
                return render(req, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = "用户名已经存在"
                    return render(req, 'login/register.html', locals())

                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    print('user exitlllldddd')
                    message = "邮箱已经注册"
                    return render(req, 'login/register.html', locals())
            new_user = models.User()
            new_user.name = username
            new_user.password = password1
            new_user.email = email
            new_user.sex = sex
            new_user.save()
            # generate number
            code = make_confirm_string(new_user)
            # send mail
            SendMail.send_email(email, code)
            message = '请前往邮箱进行确认！'
            return render(req, 'login/login.html', locals())
    register_form = forms.RegisterForm()
    return render(req, 'login/register.html', locals())


import datetime


def make_confirm_string(user):
    pass
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user)
    return code


import hashlib


def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def logout(req):
    if not req.session.get('is_login', None):
        return redirect('/login/')
    req.session.flush()
    return redirect('/login/')


#  验证码
def check_code(req):
    """
       获取验证码
       :param request:
       :return:
       """
    stream = io.BytesIO()
    # 创建随机字符 code
    # 创建一张图片格式的字符串，将随机字符串写到图片上
    img, code = CheckCode.create_validate_code()
    img.save(stream, "PNG")
    # 将字符串形式的验证码放在Session中
    req.session["CheckCode"] = code
    return HttpResponse(stream.getvalue())


# 注册用户确认
def user_confirm(req):
    code = req.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '无效的请求！！！'
        return render(req, 'login/confirm.html', locals())
    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(minutes=1):
        # if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = "您的邮件已经过期！请重新注册!"
        return render(req, 'login/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
        return render(req, 'login/confirm.html', locals())
