from django.contrib import admin

# Register your models here.

from django.contrib import admin
from repository import models

#用户名：root，密码：1234！5678
admin.site.register(models.UserInfo)
admin.site.register(models.Blog)
admin.site.register(models.WarningTable)
admin.site.register(models.ArticleType)
admin.site.register(models.ArticleTag)
admin.site.register(models.Article)
admin.site.register(models.ArticleDetail)
admin.site.register(models.UpDown)
admin.site.register(models.ArticleM2MTag)
admin.site.register(models.Comment)
