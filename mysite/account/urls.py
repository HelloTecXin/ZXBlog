from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "account"

urlpatterns = [
    # path("login/", views.user_login, name="user_login"),
    # django 内置登录方法
    path("login/", auth_views.LoginView.as_view(template_name='account/login2.html'), name="user_login"),
    # 在Django中，默认配置了登录之后页面的转向地址，在官方文档中对此有明确说明。即LOGIN_REDIRECT_URL的默认值是
    # /account/profile/ 为了设置项目所需要的转向目标，需要在settings中增加LOGIN_REDIRECT_URL 的值
    # Django 内置退出方法
    path("logout/", auth_views.LogoutView.as_view(template_name='account/logout.html'), name="user_logout"),
    path("register/", views.register, name="user_register"),
    path("password-change/", auth_views.PasswordChangeView.as_view(template_name="account/password_change_form.html",
                                                                   success_url="/account/password-change-done/"),
         name="password_change"),
    path("password-change-done/",
         auth_views.PasswordChangeDoneView.as_view(template_name="account/password_change_done.html"),
         name="password_change_done"),
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name="account/password_reset_form.html",
                                                                 email_template_name="account/password_reset_email.html",
                                                                 success_url="/account/password-reset-done/"),
         name="password_reset"),
    # email_template_name :设置向申请重置密码的用户邮箱所发送的邮件内容
    path("password-reset-done/", auth_views.PasswordResetDoneView.as_view
            (template_name="account/password_reset_done.html"), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view
        (template_name="account/password_reset_confirm.html",success_url="/account/password-reset-complete/"),
         name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view
    (template_name="account/password_reset_complete.html"),name="password_reset_complete"),
    path("my-information/",views.myself,name="my_information"),
    path("edit-my-information/",views.myself_edit,name="edit_my_information"),
    path("my-image/",views.my_image,name="my_image"),



]

