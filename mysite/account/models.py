from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserProfile(models.Model):  # 建立account_userprofile数据库表
    """注册时补充模型类"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)  # Userprofile类与User类之间的关系是“一对一”
    birth = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=20, null=True)

    def __str__(self):
        return 'user{}'.format(self.user.username)


class UserInfo(models.Model):
    """个人信息模型类"""
    user = models.OneToOneField(User,on_delete=models.CASCADE,unique=True)
    school = models.CharField(max_length=100,blank=True)
    company = models.CharField(max_length=100,blank=True)
    profession = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    aboutme = models.TextField(blank=True)
    photo = models.ImageField(upload_to='avatar/%Y%m%d', blank=True)

    def __str__(self):
        return "user:{}".format(self.user.username)
