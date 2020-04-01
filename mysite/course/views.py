from django.shortcuts import render,redirect
from django.views.generic import TemplateView, ListView
# Create your views here.
from .models import Course,Lesson
from django.contrib.auth.models import User
import json
from django.http import HttpResponse
from braces.views import LoginRequiredMixin
from django.views.generic.edit import CreateView, DeleteView
from django.shortcuts import redirect
from .forms import CreateCourseForm,CreateLessonForm
from django.urls import reverse_lazy
from django.views import View  # 所有基于类的视图的基类
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateResponseMixin # 提供了一种模板渲染的机制，在子类中，可以指定模板文件和渲染数据


class AboutView(TemplateView):
    template_name = "course/about.html"


class CourseListView(ListView):
    model = Course  # 声明类中使用的数据模型， 能够得到响应的数据库表中的所有记录。
    # queryset = Course.objects.filter(user=User.objects.get(username='张鑫'))
    context_object_name = "courses"  # 传入模板中变量名称
    template_name = 'course/course_list.html'

    # 不重写queryset则 model=Course 得到所有记录不筛选
    # def get_queryset(self):
    #     qs = super(CourseListView, self).get_queryset() # 调用了父类的get_queryset()方法，
    #     return qs.filter(user = User.objects.get(username="张鑫"))   # 根据得到的对象依据条件进行筛选


class UserMixin:  # 这个类将被用于后面的类中，而不是作为视图使用
    def get_queryset(self):
        qs = super(UserMixin, self).get_queryset()
        return qs.filter(user=self.request.user)


class UserCourseMixin(UserMixin, LoginRequiredMixin):  # 还是一个Mixin，但它继承了UserMixin， 上面定义的方法也被带入到当前类中
    model = Course
    login_url = "/account/login/"


class ManageCourseListView(UserCourseMixin, ListView):  # 继承顺序，一般Mixin类放在左边，其他类放在右边
    # 多重继承， 类UserCourseMixin所代入的就是在上面两个类中所定义的方法和属性
    # 类似的，还可以创建其他的类，继承上面的两个类，从而不必在类中重复相同的代码 this is Mixin
    context_object_name = "courses"
    template_name = 'course/manage/manage_course_list.html'


# 在Django的视图函数中返回json值
def foo_view(request):
    data = {"name": 'alaoshi', 'web': 'django'}
    return HttpResponse(json.dumps(data), content_type='application/json')


class CreateCourseView(UserCourseMixin, CreateView):
    """当用户以GET方式请求时，即在页面中显示表单，CreateView就是完成这个作用的类，只要继承它，就不需要写get()方法了"""
    fields = ['title', 'overview']  # 声明在表单中显示的字段
    template_name = 'course/manage/create_course.html'

    def post(self, request, *args, **kwargs):  # 专门处理以POST方式提交的表单内容
        form = CreateCourseForm(data=request.POST)
        if form.is_valid():
            new_course = form.save(commit=False)
            new_course.user = self.request.user
            new_course.save()
            return redirect("course:manage_course")  # 当表单内容被保存后，将页面转向指定位置
        return self.render_to_response({"form": form})  # 当表单数据检测不通过是没让用户重新填写


class DeleteCourseView(UserCourseMixin, DeleteView):
    # template_name = 'course/manage/delete_course_confirm.html'
    success_url = reverse_lazy("course:manage_course")
    # template_name = 'course/course_list.html'

    def dispatch(self, *args, **kwargs):
        resp = super(DeleteCourseView, self).dispatch(*args, **kwargs)
        if self.request.is_ajax():
            response_data = {"result": "ok"}
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            return resp

# class DeleteCourseView(UserCourseMixin, DeleteView):
#     success_url = reverse_lazy("course:manage_course")
#
#     # 继承DelteView类后，后续代码就不需要重复删除后动作了，只需要声明确认删除的模板template_name
#     # 和删除完成之后的界面success_url
#     def dispatch(self, *args, **kwargs):  # 重写DleteVIew中的dispatch()方法
#         """原本在DeleteView类中执行dispatch()方法后，会实现URL的转向，但是在此指令发送给前端之前，
#         会通过 下面的语句进行判断，如果是ajax方法提交过来的数据，就直接反馈HttpResponse对象给前端，前端的js函数
#         得到反馈结果，这样就完成了删除和页面刷新功能"""
#         resp = super(DeleteCourseView, self).dispatch(*args, **kwargs)
#         if self.request.is_ajax():
#             response_data = {"result":"ok"}
#             return HttpResponse(json.dumps(response_data),content_type="application/json")
#         else:
#             return resp


class CreateLessonView(LoginRequiredMixin,View):
    model = Lesson
    login_url = "/account/login/"

    def get(self,request,*args,**kwargs): # get要接收前端提交的数据，所以第二个参数为request
        form = CreateLessonForm(user=self.request.user)
        # 创建了表单类的实例，表单类中重写了初始化函数，增加了参数user，所以实例化时需要传入user值
        return render(request, "course/manage/create_lesson.html",{"form":form})

    def post(self,request,*args,**kwargs):
        form = CreateLessonForm(self.request.user,request.POST,request.FILES)
        # 提交的表单中有上传的文件，所以必须传入request.FILES
        if form.is_valid():
            new_lesson = form.save(commit=False)
            new_lesson.user = self.request.user
            new_lesson.save()
            return redirect("course:manage_course")


class ListLessonsView(LoginRequiredMixin, TemplateResponseMixin, View):
    login_url = "/account/login/"
    template_name = 'course/manage/list_lessons.html'  # 定义模板文件

    def get(self,request,course_id):    # 响应前端get请求的方法，因为要识别课程标题，所以传入了course_id
        course = get_object_or_404(Course,id=course_id) # 根据course_id 得到当前的课程标题对象
        return self.render_to_response({'course':course})
        # 将该数据渲染到模板中，render_to_response()就是TemplateResponseMixin类的方法


class DetailLessonView(LoginRequiredMixin,TemplateResponseMixin,View):
    login_url = "/account/login/"
    template_name = "course/manage/detail_lesson.html"

    def get(self,reuqest,lesson_id):
        lesson = get_object_or_404(Lesson,id=lesson_id)
        return self.render_to_response({"lesson":lesson})


class LessonDetailView(DetailLessonView):
    template_name = "course/lesson_detail.html"


class StudentListLessonView(ListLessonsView):
    """继承上面已经创建的类ListLessonsView类，因为显示的模板文件不同，所以重写模板"""
    template_name = "course/slist_lessons.html"

    def post(self,reqeust,*args,**kwargs):
        course = Course.objects.get(id=kwargs['course_id'])
        course.student.add(self.request.user)
        return HttpResponse("ok")