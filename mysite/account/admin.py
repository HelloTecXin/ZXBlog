from django.contrib import admin
from .models import UserProfile,UserInfo
# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth', 'phone')   # 列出列表中的项目
    list_filter = ('phone', )   # 规定网页右边FILTER的显示内容

admin.site.register(UserProfile, UserProfileAdmin)


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'school', 'company', 'profession', 'address', 'aboutme', 'photo')
    list_filter = ('school', 'company', 'profession')

admin.site.register(UserInfo,UserInfoAdmin)