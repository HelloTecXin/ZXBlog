from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from .models import ArticlePost,ArticleColumn
from django.contrib.auth.models import User


def article_titles(request,username=None):
    """文章列表"""
    if username:
        """查看作者文章"""
        user = User.objects.get(username=username)
        articles_title = ArticlePost.objects.filter(author=user)
        try:
            # 模型类UserInfo与User建立了一对一的关系
            # 通过User类的实例得到UserInfo类的信息，可以使用类似user。userinfo的模式
            # user是User类的实例。而 userinfo就是Userinfo 规定使用小写
            userinfo = user.userinfo
        except:
            userinfo = None
    else:
        articles_title = ArticlePost.objects.all()
    paginator = Paginator(articles_title,2)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list
    if username:
        return render(request,"article/list/author_articles.html",{
            "articles":articles,"page":current_page,"userinfo":userinfo,"users":user
        })
    return render(request,"article/list/article_titles.html",{
        "articles":articles,"page":current_page})


def article_detail(request,id,slug):
    """文章详情页面"""
    article = get_object_or_404(ArticlePost,id=id,slug=slug)
    return render(request,"article/list/article_content.html",{
        "article":article
    })