from django.urls import path
from . import views

app_name = "blog"  # 方式二需要加此项
urlpatterns = [
    path("", views.blog_title, name="blog_title"),
    path('<int:article_id>/', views.blog_article, name="blog_article"),

]
