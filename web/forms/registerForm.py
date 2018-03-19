#定义的注册页面的django Form表单类
#定义要验证的内容格式的类，django的form组件功能
from django.forms import fields
from django.forms import widgets
from django import forms #导入django的form功能
from django.core.validators import RegexValidator  #django form组件自定义验证规则使用
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError #导入错误码
from repository import models #导入自定义的表结构

class RegisterForm(forms.Form):
    username = fields.CharField(
        max_length=60,
        error_messages={'required':'用户信息不能为空'},
        widget=widgets.TextInput(attrs={
            'name':'username',
            'class':"form-control",
            'id':"username",
            'placeholder':"请输入用户名"
            }), #定义html中标签的参数
    )
    pwd = fields.CharField(
        max_length=12,
        min_length=6,
        error_messages={'required':'密码不能为空',
                        'min_length':'密码长度不能小于6',
                        'max_length':'密码长度不能大于12'
                        },
        widget=widgets.PasswordInput(attrs={
            'name':'pwd',
            'class':"form-control",
            'id':"pwd",
            'placeholder':"请输入密码",
        }),
        validators=[RegexValidator(r'[0-9]+','密码必须是 数字+字母 的组合'),
                    RegexValidator(r'[a-zA-Z]+', '密码必须是 数字+字母 的组合')]
    )
    confirm_pwd = fields.CharField(
        max_length=12,
        min_length=6,
        error_messages={'required': '密码不能为空',
                        'min_length': '密码长度不能小于6',
                        'max_length': '密码长度不能大于12'
                        },
        widget=widgets.PasswordInput(attrs={
            'name': 'confirm_pwd',
            'class': "form-control",
            'id': "confirm_pwd",
            'placeholder': "请再次输入密码",
        }),
    )
    email = fields.EmailField(
        error_messages={'required':'邮箱不能为空',
                        'invalid':'邮箱格式不正确',
                        },
        widget=widgets.TextInput(attrs={
            'name': 'email',
            'class': "form-control",
            'id': "email",
            'placeholder': "请输入邮箱"
        }),
    )

#验证数据库中是否已经存在这个用户了
    def clean_username(self):
        username = self.cleaned_data.get("username")#取出username的值
        submit_user_obj = models.UserInfo.objects.filter(
            username=username).first()  # 在数据库中查找这个用户名是否已经存在，如果已经存在，会返回这个对象，即非空值
        if submit_user_obj:  # 如果数据库中已经有这个用户
            raise ValidationError('这个用户名已经存在了') #把错误提示赋给obj.errors["username"]
        return username  #要反回这个数据

#验证2次输入的密码是否相等
    def clean(self):
        value_dict = self.cleaned_data  # 取出用户填的所有内容,是个字典
        username = value_dict.get('username')  # 取出用户输入的数据
        pwd = value_dict.get('pwd')
        confirm_pwd = value_dict.get('confirm_pwd')
        if pwd != confirm_pwd:
            raise ValidationError('两次输入的密码不一致')  # 这个整体的错误信息赋给obj.errors[__all__]，html里用{{obj.non_field_errors}}表示

