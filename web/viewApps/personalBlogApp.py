from django.shortcuts import render,HttpResponse,redirect
from repository import models
import django.db

#个人博客主页

#列出文章列表
def articleList(request,*args,**kwargs):
    print("i am in articleList")
    blogUser = kwargs.get("blogUser") #取出blog的用户名
    # print("tag are: ",obj_blog.blog2articleTag.all()) #多对多跨表操作必须要加.all()、.first()等筛选条件
    userChoice = kwargs.get("choiceTitle")#choiceTitle传递用户选的是文章类型还是标签还是时间
    choiceSubTitle = kwargs.get("choiceSubTitle")#choiceSubTitle传递用户选的具体的那个小标题，例如，选的类型下面的哪个类型
    obj_blog = models.UserInfo.objects.filter(username=blogUser).first().userinfo2blog  # 取出这个人的blog

    article_obj = models.Article.objects.filter(nid=3).first()
    print("article time is",article_obj.ctime)
    if kwargs.get("articleNid"):
        print("articleNid is:",kwargs.get("articleNid"))

    if userChoice == "articleType":
        article_show_obj = obj_blog.blog2article.filter(article2articletype_id=choiceSubTitle)  #按类型 取出要在个人博客主页展示的文章的对象
        print("articleType is : ",userChoice)
    elif userChoice == "articleTag":
        article_show_obj = obj_blog.blog2article.filter(article2articletag__nid=choiceSubTitle)  #按标签 取出要在个人博客主页展示的文章的对象
    else:
        article_show_obj = obj_blog.blog2article.all() #如果没有筛选，取出所有的文章
    #obj_blog用于显示左侧的菜单栏
    return render(request, "personBlog/articleList.html", {"obj_blog":obj_blog, "article_show_obj":article_show_obj})



def articleDetail(request,*args,**kwargs):
    articleNid = kwargs.get("articleNid")  #article的nid
    print("i am in article detail")
    print(articleNid)
    blogUser = kwargs.get("blogUser")
    obj_blog = models.UserInfo.objects.filter(username=blogUser).first().userinfo2blog  # 取出这个人的blog
    article_obj = models.Article.objects.filter(nid=articleNid).first()
    try:
        articleDetailContent = article_obj.article2detail.content  #通过article的nid找到这个article，再找到这个article对应的articleDetail
        print("detail",articleDetailContent)
    except AttributeError:  #捕获如果这个article没有articleDetail的错误
        articleDetailContent = "没有详细内容"
    return render(request,"personBlog/articleDetail.html",{"obj_blog":obj_blog,"articleDetailContent":articleDetailContent})