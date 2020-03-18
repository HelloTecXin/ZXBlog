from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from .models import ArticlePost,ArticleColumn
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


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


@csrf_exempt
@require_POST
@login_required(login_url="/account/login/")
def like_article(request):
    """点赞功能
    1、用于给article这个实例的属性user_like增加一个用户，
    如果不同对象之间建立了一对多或者多对多的关联关系，那么就可以使用add（*objs，bulk=TRUE）
    方法增加属性的值，从而建立起两个对象的关系"""
    article_id = request.POST.get("id")
    action = request.POST.get("action")
    if article_id and action:
        try:
            article = ArticlePost.objects.get(id=article_id)
            if action =="like":
                # 1
                article.users_like.add(request.user)
                return HttpResponse("1")
            else:
                article.users_like.remove(request.user)
                return HttpResponse("2")
        except:
            return HttpResponse("no")

