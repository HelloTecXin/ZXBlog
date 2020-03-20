from django import template
register = template.Library()

from article.models import ArticlePost


@register.simple_tag
def total_articles():
    return ArticlePost.objects.count()


@register.simple_tag
def author_total_articles(user):
    return user.article.count()


@register.inclusion_tag('article/list/latest_articles.html')
# 增加了参数，确定所渲染的模板文件 ，返回的数据被应用到指定的模板文件中
def latest_articles(n=5): # 定义参数，具体使用标签时会向这里传入参数
    latest_articles = ArticlePost.objects.order_by('-created')[:n]
    return {"latest_articles":latest_articles}