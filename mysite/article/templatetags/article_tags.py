from django import template
register = template.Library()

from article.models import ArticlePost
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown


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


@register.simple_tag
def most_commented_articles(n=3):
    return ArticlePost.objects.annotate(total_comments=Count('comments')).order_by("-total_comments")[:n]
# annotate相当于all() 但是添加了其中的注释，相当于每个对象都有了total_commnets属性
# 其实就是该ArticlePost对象所关联的Comment对象的数量，即评论的数量
# 因此通过 article.total_comments就得到了ArticlePost对象的Comment对象数量


@register.filter(name='markdown')
# 重命名定义函数中   选择器函数 ，即将名字由markdown_filter修改为markdown
# 因为前面导入了markdown，所以此处不使用markdown作为函数名称
def markdown_filter(text):
    return mark_safe(markdown.markdown(text)) # 返回的是“safe string”并且是用过markdown()方法之后返回的结果。使Django模板能够顺利接收
# django 对于在模板上显示字符串这件事是非常谨慎的django.utils.safestring的作用就是将字符串编程为“safe string”
# 即实实在在的字符，而不是HTML代码 mark_safe()方法返回的就是这种“safe string”
#