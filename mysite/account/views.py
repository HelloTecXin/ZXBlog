from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegistrationForm, UserProfileForm,UserForm,UserInfoForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile,UserInfo
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.


def user_login(request):
    """登录视图，实际使用的Django自带的登录函数"""
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(username=cd["username"], password=cd["password"])
            if user:
                login(request, user)
                return HttpResponse("Welcome You. You have been authenticated successfully")
            else:
                return HttpResponse("Sorry. You username or password is not right.")
        else:
            return HttpResponse("Invalid login")
    if request.method == "GET":
        login_form = LoginForm()
        return render(request, "account/login.html", {"form": login_form})


def register(request):
    """注册视图"""
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        if user_form.is_valid() * userprofile_form.is_valid():
            new_user = user_form.save(commit=False)
            # ModelForm类和它的子类都具有save()方法，将表单数据保存到数据库，并且生成该对象
            # commit = False 数据并没有被保存到数据库，而仅生成了一个数据对象
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            new_profile = userprofile_form.save(commit=False)
            new_profile.user = new_user
            new_profile.save()
            return HttpResponseRedirect(reverse("account:user_login"))
        else:
            return HttpResponse("sorry,your can not register.")
    else:
        user_form = RegistrationForm()
        userprofile_form = UserProfileForm()
        return render(request, "account/register.html", {"form": user_form, "profile": userprofile_form})


@login_required()
def myself(request):
    """用户个人中心表单（不太理解）"""
    userprofile = UserProfile.objects.get(user=request.user) if hasattr(request.user, 'userprofile') \
        else UserProfile.objects.create(user=request.user)
    userinfo = UserInfo.objects.get(user=request.user) if hasattr(request.user,'userinfo') \
        else UserInfo.objects.create(user=request.user)
    return render(request, "account/myself.html",{"user":request.user,"userinfo":userinfo,"userprofile":userprofile})


@login_required(login_url='/account/login/')
def myself_edit(request):
    userprofile = UserProfile.objects.get(user=request.user) if hasattr(request.user,'userprofile') \
        else UserProfile.objects.create(user=request.user)
    userinfo = UserInfo.objects.get(user=request.user) if hasattr(request.user,'userinfo') \
        else UserInfo.objects.create(user=request.user)

    if request.method == "POST":
        user_form = UserForm(request.POST)  # 提交email
        userprofile_form = UserProfileForm(request.POST) # 补充注册 phone birth
        userinfo_form = UserInfoForm(request.POST) # 个人信息 school等等
        if user_form.is_valid() * userprofile_form.is_valid() * userinfo_form.is_valid(): #  检查数据是否符合要求
            user_cd = user_form.cleaned_data # 返回实例的属性字典
            userprofile_cd = userprofile_form.cleaned_data
            userinfo_cd = userinfo_form.cleaned_data
            request.user.email = user_cd['email']
            userprofile.birth = userprofile_cd['birth']
            userprofile.phone = userprofile_cd['phone']
            userinfo.school = userinfo_cd['school']
            userinfo.company = userinfo_cd['company']
            userinfo.profession = userinfo_cd['profession']
            userinfo.address = userinfo_cd['address']
            userinfo.aboutme = userinfo_cd['aboutme']
            request.user.save()
            userprofile.save()
            userinfo.save()
        return HttpResponseRedirect("/account/my-information/")
    else:
        user_form = UserForm(instance=request.user)
        userprofile_form = UserProfileForm(initial={"birth":userprofile.birth,"phone":userprofile.phone})
        userinfo_form = UserInfoForm(initial={"school":userinfo.school,"company":userinfo.company,
                              "profession":userinfo.profession,"address":userinfo.address,"aboutme":userinfo.aboutme})
        return render(request,"account/myself_edit.html",{"user_form":user_form,"userprofile_form":userprofile_form,
                                                          "userinfo_form":userinfo_form})


@login_required(login_url="/account/login/")
def my_image(request):
    userinfo = UserInfo.objects.get(user=request.user.id)
    userinfo.photo = request.FILES["photo"]
    userinfo.save()
    return HttpResponseRedirect("/account/my-information/")
