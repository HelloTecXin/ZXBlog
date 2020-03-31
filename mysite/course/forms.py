from django import forms
from .models import Course,Lesson


class CreateCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('title','overview')


class CreateLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['course','title','video','description','attach']

    def __init__(self,user,*args,**kwargs):  # 通过user 参数传入当前用户，用于下 筛选出当前用户的course值
        """重写__init__()初始化函数，让每个用户只能看到自己所设置的课程标题"""
        super(CreateLessonForm, self).__init__(*args,**kwargs)
        self.fields['course'].queryset = Course.objects.filter(user=user)