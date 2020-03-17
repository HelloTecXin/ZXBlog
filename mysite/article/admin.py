from django.contrib import admin
from .models import ArticleColumn,ArticlePost
# Register your models here.


class ArticlColumnAdmin(admin.ModelAdmin):
    list_display = ('column','created','user')
    list_filter = ("column",)

admin.site.register(ArticleColumn,ArticlColumnAdmin)


# 可以不存在(不存在的话作者自己管理自己的文章)
class ArticlePostAdmin(admin.ModelAdmin):
    list_display = ("author",'title',"slug","column","body","created")
    list_filter = ('author','title')

admin.site.register(ArticlePost,ArticlePostAdmin)