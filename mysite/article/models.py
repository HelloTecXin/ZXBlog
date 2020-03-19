from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.utils import timezone
from django.urls import reverse
from slugify import slugify


class ArticleColumn(models.Model):
    """栏目"""
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='article_column')
    column = models.CharField(max_length=200)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.column


class ArticlePost(models.Model):
    """文章"""
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="article")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=500)
    column = models.ForeignKey(ArticleColumn,on_delete=models.CASCADE, related_name="article_column")
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    update = models.DateTimeField(auto_now=True)
    users_like = models.ManyToManyField(User,related_name="articles_like", blank=True)   # 用户点赞功能

    class Meta:
        ordering = ("-update",)         # 查询结果的排序
        index_together = (('id', 'slug'),)
        # 对数据库中这两个字段建立索引，后面会通过每篇文章的id和slug获取该文章对象，
        # 建立索引能够提高读取文章对象的速度

    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)
        super(ArticlePost, self).save(*args,**kwargs)
        # 每个模型类都有一个save方法，对此方法进行重写，实现slug的赋值

    def get_absolute_url(self):
        return reverse("article:article_detail",args=[self.id, self.slug])
        # 获取谋篇文章对象的url

    def get_url_path(self):
        return reverse("article:article_content",args=[self.id,self.slug])


class Comment(models.Model):
    """文章评论"""
    article = models.ForeignKey(ArticlePost,on_delete=models.CASCADE,related_name="comments")
    commentator = models.CharField(max_length=90)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return "Comment by{0}on{1}".format(self.commentator.username,self.article)
