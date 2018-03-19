################登录页面##############################
from web.forms.loginForm import LoginForm  #导入自定义的django Form 类
from django.shortcuts import render
from django.shortcuts import redirect

from repository import models  #导入我们写的描述表结构的类
#登录页面函数
def login(request):
    if request.method == "GET":
        obj = LoginForm()
        return render(request, 'login.html', {'obj':obj})
    elif request.method == "POST":
        obj = LoginForm(request.POST)#生成一个LoginForm的对象,把reques.POST的数据传给这个类
        ret = obj.is_valid()#让obj去验证输入内容的格式,如果验证通过，返回True。如果有验证失败的内容，返回False。django的Form表单只能验证输入的格式，输入的内容正确与否还有去和数据库中的内容对比
        if ret: #如果django form表单验证通过
    # cleaned_data是个字典,里面是表单的{name:value,name2:value2}。
            print('clean_data is ',obj.cleaned_data)
            username = obj.cleaned_data.get('username') #取出用户输入的数据
            pwd = obj.cleaned_data.get('pwd')
            print('username',username)
            print('pwd is',pwd)
            auth_result = {'username_err':'','pwd_err':''} #记录去数据库验证用户名密码的结果，如果验证正确，则为空，如果不正确，返回错误提示
            submit_user_obj = models.UserInfo.objects.filter(username=username).first() #在数据库中查找用户输入的用户
            if submit_user_obj: # 如果数据库中有这个用户
                if pwd != submit_user_obj.pwd: #如果密码不正确
                    auth_result['pwd_err'] = '密码不正确'
                else:  #如果用户名认证通过
                    request.session['username'] = username  #把用户名写到session里
                    request.session['is_login'] = True  #把登录状态写到session里
                    print('request.POST.get reamin is',request.POST.get('remain'))
                    if request.POST.get('remain') == 'yes':#如果勾选了xxx时间内免登陆，如果不勾选，django默认超时时间是2周
                        # request.session.set_expiry(60*60*24*10) #超时时间，单位秒
                        request.session.set_expiry(10) #超时时间，单位秒,设为10s，测试用
                    return redirect('/web/index')
                    # return HttpResponse('OK')
            else: #如果数据库中没有这个用户
                auth_result['username_err'] = '用户名不正确'
            return render(request, 'login.html', {'obj':obj, 'auth_result':auth_result})
        else: #如果django form表单验证没有通过
            return render(request, 'login.html', {'obj':obj})

################登录页面-结束##############################
