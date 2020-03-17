"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

# 为上传的图片配置url路径(1)
from django.conf import settings
from django.conf.urls.static import static
# 通用视图
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    # 为了实现{% url 'blog:blog_title' %}的效果，需要在项目和应用两级的urls.py文件进行相应配置
    # path('blog/',include(('blog.urls', 'blog'), namespace='blog')),   # 方式一

    path('blog/', include('blog.urls', namespace='blog')),      # 方式二
    path('account/', include('account.urls', namespace='account')),
    path('article/',include('article.urls',namespace='article')),
    path('home/', TemplateView.as_view(template_name='home.html'),name='home'),

]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


