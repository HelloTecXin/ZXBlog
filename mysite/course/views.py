from django.shortcuts import render
from django.views.generic import TemplateView,ListView
# Create your views here.
from .models import Course


class AboutView(TemplateView):
    template_name = "course/about.html"


class CourseListView(ListView):
    model = Course  # 声明类中使用的数据模型， 能够得到响应的数据库表中的所有记录。
    context_object_name = "courses" # 传入模板中变量名称
    template_name = 'course/course_list.html'
