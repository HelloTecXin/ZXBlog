from django.shortcuts import render,get_object_or_404
from .models import BlogArticles
# Create your views here.


def blog_title(request):
    blogs = BlogArticles.objects.all()
    # render 的第一个参数必须是request，然后是模板的位置和传送的数据，数据是用类字典的形式传送给模板
    return render(request, "blog/titles.html", {"blogs": blogs})


def blog_article(request,article_id):
    # article = BlogArticles.objects.get(id=article_id)
    article = get_object_or_404(BlogArticles, id=article_id)  # 简化对请求网页不存在是的异常处理
    pub = article.publish
    return render(request, "blog/content.html", {"article": article, "publish": pub})
