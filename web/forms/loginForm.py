from django.forms import fields
from django.forms import widgets
from django import forms #导入django的form功能
from django.core.validators import RegexValidator  #django form组件自定义验证规则使用

#定义要验证的内容格式的类，django的form组件功能
class LoginForm(forms.Form):
    username = fields.CharField(
        max_length=60,
        error_messages={'required':'用户信息不能为空'},
        widget=widgets.TextInput(attrs={'name':'username',
                                        'class':"form-control",
                                        'id':"username",
                                        'placeholder':"请输入用户名"
                                        }),
    )
    pwd = fields.CharField(
        max_length=12,
        min_length=3,
        error_messages={'required':'密码不能为空',
                        'min_length':'密码长度不能小于3',
                        'max_length':'密码长度不能大于12'
                        },
        widget=widgets.PasswordInput(attrs={
            'name':'pwd',
            'class':"form-control",
            'id':"pwd",
            'placeholder':"请输入密码",
        }),
    )