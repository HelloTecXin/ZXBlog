from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from slugify import slugify


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
