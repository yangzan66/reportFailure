from django.shortcuts import render,HttpResponse,redirect

# from django.db import models
from repository import models  #导入我们写的描述表结构的类

import json
from django.core.handlers.wsgi import  WSGIRequest
from django.urls import  reverse
from utils.page import Page #导入我写的Page类，用于主站分页显示

from .forms.registerForm import RegisterForm  #导入自定义的django Form 类


#认证函数,装饰器
def auth(func):
    def inner(request,*args,**kwargs):
        if request.session.get('is_login'): #如果session里有这个用户的登录状态
            return func(request,*args,**kwargs) #执行被装饰函数
        else:
            # return redirect('/web/login/')# 否则，返回登录页面
            return redirect(reverse('web:login'))# 否则，返回登录页面
    return inner



#################注册页面-开始##############################

#注册页面函数
def register(request):
    if request.method == "GET":
        obj = RegisterForm()
        return render(request, 'register.html', {'obj': obj,}) #返回obj，生成页面
    elif request.method == "POST":
        obj = RegisterForm(request.POST)#生成一个RegisterForm的对象,把reques.POST的数据传给这个类
        ret = obj.is_valid()#让obj去验证输入内容的格式,如果验证通过，返回True。如果有验证失败的内容，返回False。django的Form表单可以验证输入的格式
        # print('clean_data1111 is ', obj.cleaned_data)
        if ret: #如果django form表单验证通过
    # cleaned_data是个字典,里面是表单的{name:value,name2:value2}。
            username = obj.cleaned_data.get('username') #取出用户输入的数据
            pwd = obj.cleaned_data.get('pwd')
            email = obj.cleaned_data.get('email')
            models.UserInfo.objects.create(username=username,email=email,pwd=pwd)  #把注册用户的信息写到数据库中
            # return redirect('/web/login/')
            return redirect(reverse('web:login'))
        else: #如果django form表单验证没有通过
            return render(request, 'register.html', {'obj': obj})

#################注册页面-结束##############################


#注销登录 - 开始
# 注销后必须重新输入用户名密码才能再次登录
def logout(request):
    # del request.session['username'] #删除session中 username的值
    request.session.clear() #清空当前用户所有的session信息
    # return redirect('/web/login/')
    return redirect(reverse('web:login'))

#注销登录 - 结束


#主页显示 - 开始
# @auth
def index(request,*args,**kwargs):
    if request.method == 'GET':
        #添加数据，用于测试
        # for i in range(30,200):
        #     data = {
        #         'title' : 'mysql title' + str(i),
        #         'summary' : 'mysql summary' + str(i),
        #         'home_choice_id':3,   #主页文章类型
        #         'article2userinfo_id':1,
        #         'article2blog_id':1,
        #         'article2articletype_id':1,
        #     }
        #     models.Article.objects.create(**data)
        # 添加数据 -结束


        if kwargs.get('article_id'):  #article_id是urls.py中正则传过来的，表示用户在主站上哪个类型标签。如果article_id存在，再把它转为整数
            article_id = int(kwargs.get('article_id')) #article_id是用户点的主站的文章类型标签的id，article_id转成整数，方便html中和item.0比较
        else:
            article_id = kwargs.get('article_id')
        if article_id == 0 or not article_id: #如果article_id是0，表示用户点的‘全部’标签
            choice_all_data = models.Article.objects.all()  #choice_all_data表示用户点的类型的所有数据
            article_id = 0 #如果article_id是NULL，也赋成0
        else:
            choice_all_data = models.Article.objects.filter(home_choice_id = article_id)

        article_home_choice = models.Article().home_choice #获取主页的文章有哪些分类，用于在主页上显示
        # print('article id is',article_id)
        #分页显示 - 开始
        base_url = reverse('web:index', kwargs=kwargs)  #拼出分页显示时的base_url,url的前缀
        current_page = int(request.GET.get('p', 1))  # 获取要展示第几页,如果没指定p，那么默认显示第一页
        data_count = len(choice_all_data)
        per_page_count = request.COOKIES.get('per_page_count', 10)  # 获取显示多少行的cookie的值,没有cookie时默认显示10行
        if per_page_count != '10' and per_page_count != '30' and per_page_count != '50' and per_page_count != '80':  # 如果读到的cookie不是10/30/50/80
            per_page_count = 10  # 默认每页显示10行
        else:
            per_page_count = int(per_page_count)
        page_obj = Page(current_page=current_page, data_count=data_count, per_page_count=per_page_count,
                        pager_num=11)  # len(LIST)数据的总个数
        data = choice_all_data[page_obj.start():page_obj.end()]  # 获取到当前页要显示的数据
        page_str = page_obj.page_str(base_url)  # 把url的前缀作为参数传给函数，返回要添加到html里的页面的索引
        # li:要显示的当前页的数据。
        # page_str:要添加到html里的页面的索引语句。
        # base_url：url的前缀
        # page_count：总的页数
        #article_home_choice:获取主页的文章有哪些分类，用于在主页上显示
        # article_id:用户点的主站的文章类型标签的id
        print('33333base url is',base_url)
        print("article type id is :",article_id)
        return render(request,'index.html',{'li': data,
                                            'page_str': page_str,
                                            'base_url': base_url,
                                            'page_count': page_obj.all_count(),
                                            'article_home_choice':article_home_choice,
                                            'article_id':article_id,})
        #分页显示 - 结束
        # return render(request, 'index.html',{'data':data,'article_home_choice':article_home_choice,'article_id':article_id,})
#主页显示 - 结束