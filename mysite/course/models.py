from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from slugify import slugify
from .field import OrderField


class Course(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='course_user')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering =('-created',)

    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)
        super(Course, self).save(*args,**kwargs)

    def __str__(self):
        return self.title


def user_directory_path(instance,filename):
    """用户上传的文件存放到自己的目录里"""
    return "courses/user_{0}/{1}".format(instance.user.id,filename)


class Lesson(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='lesson_user')
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="lesson")
    title = models.CharField(max_length=200)
    video = models.FileField(upload_to=user_directory_path)    # 视频
    description = models.TextField(blank=True)
    attach = models.FileField(blank=True,upload_to=user_directory_path) # 附件
    created = models.DateTimeField(auto_now_add=True)
    order = OrderField(blank=True,for_fields=['course'])

    class Meta:
        ordering =['order']

    def __str__(self):
        return '{}.{}'.format(self.order,self.title)


