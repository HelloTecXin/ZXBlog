from django.shortcuts import render
from django.views.generic import TemplateView,ListView
# Create your views here.
from .models import Course
from django.contrib.auth.models import User
import json
from django.http import HttpResponse
from braces.views import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
from .forms import CreateCourseForm


class AboutView(TemplateView):
    template_name = "course/about.html"


class CourseListView(ListView):
    model = Course  # 声明类中使用的数据模型， 能够得到响应的数据库表中的所有记录。
    # queryset = Course.objects.filter(user=User.objects.get(username='张鑫'))
    context_object_name = "courses" # 传入模板中变量名称
    template_name = 'course/course_list.html'

    # 不重写queryset则 model=Course 得到所有记录不筛选
    # def get_queryset(self):
    #     qs = super(CourseListView, self).get_queryset() # 调用了父类的get_queryset()方法，
    #     return qs.filter(user = User.objects.get(username="张鑫"))   # 根据得到的对象依据条件进行筛选


class UserMixin:    # 这个类将被用于后面的类中，而不是作为视图使用
    def get_queryset(self):
        qs = super(UserMixin, self).get_queryset()
        return qs.filter(user=self.request.user)


class UserCourseMixin(UserMixin,LoginRequiredMixin):  # 还是一个Mixin，但它继承了UserMixin， 上面定义的方法也被带入到当前类中
    model = Course
    login_url = "/account/login/"


class ManageCourseListView(UserCourseMixin,ListView): # 继承顺序，一般Mixin类放在左边，其他类放在右边
    # 多重继承， 类UserCourseMixin所代入的就是在上面两个类中所定义的方法和属性
    # 类似的，还可以创建其他的类，继承上面的两个类，从而不必在类中重复相同的代码 this is Mixin
    context_object_name = "courses"
    template_name = 'course/manage/manage_course_list.html'


# 在Django的视图函数中返回json值
def foo_view(request):
    data = {"name":'alaoshi','web':'django'}
    return HttpResponse(json.dumps(data),content_type='application/json')


class CreateCourseView(UserCourseMixin,CreateView):
    """当用户以GET方式请求时，即在页面中显示表单，CreateView就是完成这个作用的类，只要继承它，就不需要写get()方法了"""
    fields = ['title','overview']   # 声明在表单中显示的字段
    template_name = 'course/manage/create_course.html'

    def post(self, request, *args, **kwargs):   # 专门处理以POST方式提交的表单内容
        form = CreateCourseForm(data=request.POST)
        if form.is_valid():
            new_course = form.save(commit=False)
            new_course.user = self.request.user
            new_course.save()
            return redirect("course:manage_course") # 当表单内容被保存后，将页面转向指定位置
        return self.render_to_response({"form":form})   # 当表单数据检测不通过是没让用户重新填写
