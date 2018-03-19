"""报障系统 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from web import views
from .viewApps import login  #导入视图程序文件
from .viewApps import personalBlogApp  #导入视图程序文件
app_name = 'web'  #多级路由是，必须要写上自己app的名字，否则不能reverse反生产url

urlpatterns = [
    url(r'^index$',views.index,name='index'),  #要加上$，以dex结尾，否则会和下面的有正则的url冲突
    url(r'index/(?P<article_id>\d+)',views.index,name='index'),
    url(r'login',login.login,name='login'), #执行web/viewApps/login.py中的login函数
    url(r'register',views.register,name='register'),
    url(r'logout',views.logout,name='logout'),

   #根据左侧的类型/标签/时间 进行筛选
    url(r'userBlog/(?P<blogUser>\w+)/$',personalBlogApp.articleList,name='userBlog'),
    url(r'userBlog/(?P<blogUser>\w+)/(?P<choiceTitle>\w+)$',personalBlogApp.articleList,name='userBlog'),
    url(r'userBlog/(?P<blogUser>\w+)/(?P<choiceTitle>\w+)/(?P<choiceSubTitle>\d+)$',personalBlogApp.articleList,name='userBlog'),
    #文章详细内容
    url(r'userBlog/(?P<blogUser>\w+)/(?P<articleNid>\d+).html$',personalBlogApp.articleDetail,name='userBlog'),
]
