from django.db import models

# Create your models here.

#用户表
class UserInfo(models.Model):
    nid = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=32,unique=True)
    pwd = models.CharField(max_length=32)
    email = models.EmailField()
    img = models.IntegerField(null=True) #头像
    ctime = models.DateTimeField(auto_now_add=True) #创建时间,自动创建时间
    u1_to_u2 = models.ManyToManyField(to='UserInfo',
                                      related_name='u2_to_u1',
                                      ) #自关联，定义互粉表，一个用户可以关注多个用户，多个用户可以关注一个用户


#博客信息表
class Blog(models.Model):
    nid = models.BigAutoField(primary_key=True)
    suffix = models.CharField(max_length=16) #个人博客的后缀，一般是个人的名字
    title = models.CharField(max_length=128) #博客标题
    theme = models.CharField(max_length=64) #博客主题
    summary = models.CharField(max_length=32) #总结字段
    #设置外键字段，指向UserInfo表的nid字段，加上unique，表示1对1对应关系。博客表和用户表是1对1对应关系
    blog2userinfo = models.OneToOneField(to=UserInfo,to_field='nid',on_delete=models.CASCADE,related_name='userinfo2blog')

#报障单
class WarningTable(models.Model):
    UUID = models.UUIDField(primary_key=True)  #用UUID来标识每个报账单
    title = models.CharField(max_length=128)  # 故障标题
    detail = models.CharField(max_length=3096)  #故障详细信息
    #创建外键字段creator2userinfo，指向UserInfo的nid字段.表示这个故障单时谁创建的
    creator2userinfo = models.ForeignKey(to='UserInfo',to_field='nid',on_delete=models.CASCADE,related_name='userinfo2creator')
    # processor2userinfo，指向UserInfo的nid字段.表示这个故障单时谁处理的，可以为空，表示还没有人处理呢
    processor2userinfo = models.ForeignKey(to='UserInfo',to_field='nid',on_delete=models.CASCADE,
                                       related_name='userinfo2processor',null=True)
    status_choices = (
        (1,"待处理"),
        (2,"处理中"),
        (3,"已处理"),
    )
    status_id = models.IntegerField(choices=status_choices,default=1)
    ctime = models.DateTimeField(auto_now_add=True) #创建故障单的时间
    process_time = models.DateTimeField(null=True) #处理故障时间

#个人blog中，用户文章的分类表
class ArticleType(models.Model):
    nid = models.AutoField(primary_key=True)
    caption = models.CharField(max_length=32) #分类的标题
    articletype2blog = models.ForeignKey(to='Blog',to_field='nid',on_delete=models.CASCADE,related_name='blog2articletype') #这个文章类型属于哪个博客


#更让人blog中，用户文章的标签表
class ArticleTag(models.Model):
    nid = models.AutoField(primary_key=True)
    caption = models.CharField(max_length=32)
    articleTag2blog = models.ForeignKey(to='Blog',to_field='nid',on_delete=models.CASCADE,related_name='blog2articleTag')#这个标签属于哪个博客

#文章表
class Article(models.Model):
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=64)  #文章标题
    summary = models.CharField(max_length=128) #文章总结
    ctime = models.DateTimeField(auto_now_add=True) #创建时间
    read_count = models.IntegerField(default=0)#文章读过多少次
    comment_count = models.IntegerField(default=0)#文章评论过多少次
    up_count = models.IntegerField(default=0)#文章赞过多少次
    down_count = models.IntegerField(default=0)#文章踩过多少次
    article2userinfo = models.ForeignKey(to='UserInfo',on_delete=models.CASCADE,to_field='nid',)#外键、指向用户表
    article2blog = models.ForeignKey(to='Blog',to_field='nid',on_delete=models.CASCADE,related_name='blog2article')#这个文章属于哪个博客
    article2articletype = models.ForeignKey(to='ArticleType',to_field='nid',on_delete=models.CASCADE,related_name='aritcletype2article',null=True)#这个文章属于哪个文章类型,一个文章只属于一个了类型
    article2articletag = models.ManyToManyField(to='ArticleTag',related_name='articletag2article')#文章的标签
    home_choice = (     #主站文章类型分类
        (1, "Python"),
        (2, "Linux"),
        (3, "Nginx"),
        (4, "Mysql"),
    )
    home_choice_id = models.IntegerField(choices=home_choice)

#文章详细内容表
class ArticleDetail(models.Model):
    content = models.TextField()
    detail2article = models.OneToOneField(to='Article',to_field='nid',on_delete=models.CASCADE,related_name='article2detail')#一对一外键、指向Article表

#文章顶或踩 表,自定义第三章表
class UpDown(models.Model):
    article = models.ForeignKey(to='Article',on_delete=models.CASCADE,to_field='nid')#外键、指向文章表，表示踩/顶的哪个文章
    user = models.ForeignKey(to='UserInfo',on_delete=models.CASCADE,to_field='nid')#指向用户表，表示谁踩/顶的
    up = models.BooleanField() #是否赞了，如果赞了就不能踩了

    class Meta:
        unique_together =[
            ('article','user'),#article和user联合唯一
        ]


#标签和文章的多对多关系表（自定义第三章表）
class ArticleM2MTag(models.Model):
    article = models.ForeignKey(to='Article',on_delete=models.CASCADE) #外键、指向Article表
    tag = models.ForeignKey(to='ArticleTag',on_delete=models.CASCADE)#外键、指向ArticleTag表

    class Meta:
        unique_together = [
            ('article','tag'), #表示字段article和字段tag联合唯一
        ]

#评论表
class Comment(models.Model):
    nid = models.BigAutoField(primary_key=True)
    content = models.CharField(max_length=256)  #评论的内容
    ctime = models.DateTimeField(auto_now_add=True)  # 创建时间,自动生成创建时间
    comment2article = models.ForeignKey(to='Article',to_field='nid',on_delete=models.CASCADE,related_name='article2comment')#外键、指向Article表，评论的是哪篇文章
    comment2userinfo = models.ForeignKey(to='UserInfo',to_field='nid',on_delete=models.CASCADE,related_name='userinfo2comment')#外键、指向UserInfo表，谁评论的

    reply = models.ForeignKey(to='Comment',related_name='back',on_delete=models.CASCADE,null=True)#回复评论





