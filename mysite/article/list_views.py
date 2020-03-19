from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from .models import ArticlePost,ArticleColumn
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import redis
from django.conf import settings
from .models import Comment
from .forms import CommentForm


r = redis.StrictRedis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,db=settings.REDIS_DB)


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
    # 对访问文章的次数进行记录 incr函数的作用就是让当前的键值递增，并返回递增后的值
    # redis对键的命名并没有强制的要求，比较好的做法就是 “对象类型：对象id：对象属性”
    total_views = r.incr("article:{}:views".format(article.id))
    # 1、redis连接对象方法zincrby(name,amount,value)，其作用是根据amount所设定的步长值增加有序集合（name
    # ）中的value的数值。实现了article_ranking 中article.id 以步长为1自增，即文章被访问一次，article_ranking
    # 就将该文章id的值增加1
    r.zincrby('article_ranking',1,article.id)
    # 2、通过上一步的结果，得到article_ranking中排序前10的对象
    # zrange(name,start,end,desc=False,withscores=False,score_cast_func=float)
    article_ranking = r.zrange('article_ranking',0,-1,desc=True)[:10]
    article_ranking_ids = [int(id) for id in article_ranking]
    # 条件查询，查出id在article_ranking_ids中的所有文章对象，并以文章对象为元素生成列表
    most_viewed = list(ArticlePost.objects.filter(id__in=article_ranking_ids))
    # index()函数用于从列表中找出某个值第一个匹配项的索引位置
    # x表示匿名函数的输入，即列表中的一个元素，
    most_viewed.sort(key=lambda x: article_ranking_ids.index(x.id))
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_commnet = comment_form.save(commit=False)
            new_commnet.article = article
            new_commnet.save()
    else:
        comment_form = CommentForm()

    return render(request,"article/list/article_content.html",{
        "article":article,"total_views":total_views,"most_viewed":most_viewed,"comment_form":comment_form
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

