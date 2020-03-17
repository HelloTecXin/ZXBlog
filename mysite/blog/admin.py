from django.contrib import admin
from .models import BlogArticles

# Register your models here.


class BlogAriclesAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publish")
    list_filter = ("publish", "author")  # 过滤器
    search_fields = ("title", "body")  # 可以用来搜索的字段
    raw_id_fields = ("author",)     # 根据当前字段查询细信息
    date_hierarchy = "publish"      # 进行详细时间筛选
    ordering = ['-publish', "author"]  # 排序
admin.site.register(BlogArticles,BlogAriclesAdmin)
