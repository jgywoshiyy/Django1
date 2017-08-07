# coding=utf-8
from django.shortcuts import render, redirect
from .models import UserInfo, RecPerson
from hashlib import sha1
from django.http import HttpResponse, JsonResponse
from PIL import Image, ImageDraw, ImageFont


# Create your views here.


def register(request):
    context = {'title': '注册', 'top': '0'}
    return render(request, 'sx/register.html', context)


def register_handle(request):
    dict = request.POST
    uname = dict.get('user_name')
    upwd = dict.get('pwd')
    upwd2 = dict.get('cpwd')
    email = dict.get('email')

    if upwd != upwd2:
        redirect('/user/register/')

    s1 = sha1()
    s1.update(upwd)
    wpwd_sha1 = s1.hexdigest()

    # user = UserInfo()
    user = UserInfo.objects.model()
    user.uname = uname
    user.upwd = wpwd_sha1
    user.uemail = email
    user.save()
    return redirect('/user/login/')


# 判断是否已经注册过（注册过则返回1，没注册过返回0）
def register_valid(request):
    dict = request.GET
    uname = dict.get('uname')
    result = UserInfo.objects.filter(uname=uname).count()

    context = {'valid': result}

    return JsonResponse(context)


def register_valid1(request):
    dict = request.GET

    yzm = dict.get('yzm')
    verifycode = request.session['verifycode']
    yzm1 = yzm.upper()
    verifycode1 = verifycode.upper()

    if yzm1 == verifycode1:
        panduan = True
    else:
        panduan = False

    context = {'result': panduan}

    return JsonResponse(context)


def login(request):
    context = {'title': '登陆', 'top': '0'}
    return render(request, 'sx/login.html', context)


def login_handle(request):
    dict = request.GET
    uname = dict.get('uname')
    print uname
    result = UserInfo.objects.filter(uname=uname).count()
    print result
    if result == 0:
        context = {'name_error': '0'}

    else:
        context = {'name_error': '1'}

    return JsonResponse(context)


def verify_code(request):
    # 引入随机函数模块
    import random
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(20, 100), 255)
    width = 100
    height = 25
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('FreeMono.ttf', 23)
    # 构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    # 内存文件操作
    import cStringIO
    buf = cStringIO.StringIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')
