from django.shortcuts import render
from .models import ArticleColumn,ArticlePost
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .forms import ArticleColumnForm,ArticlePostForm
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger


@login_required(login_url='/account/login/')
@csrf_exempt        # 解决提交表单中遇到csrf的问题
def article_column(request):
    """用户的栏目"""
    if request.method == "GET":
        columns = ArticleColumn.objects.filter(user=request.user)
        column_form = ArticleColumnForm()
        return render(request,"article/column/article_column.html",{"columns":columns,'column_form':column_form})
    if request.method == "POST":
        column_name = request.POST['column']
        columns = ArticleColumn.objects.filter(user_id=request.user.id,column=column_name) # user_id 为以user作为外键
        if columns:
            return HttpResponse('2')
        else:
            ArticleColumn.objects.create(user=request.user,column=column_name)
            return HttpResponse('1')


@login_required(login_url='account/login/')
@require_POST       # 保证此视图函数只通过POST方式提交数据
@csrf_exempt
def rename_article_column(request):
    """编辑栏目名称"""
    column_name = request.POST['column_name']
    column_id = request.POST["column_id"]
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.column = column_name
        line.save()
        return HttpResponse("1")
    except:
        return HttpResponse("0")


@login_required(login_url='/account/login/')
@require_POST
@csrf_exempt
def del_article_column(request):
    """删除栏目名称"""
    column_id = request.POST['column_id']
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")


@login_required(login_url="/account/login/")
@csrf_exempt
def article_post(request):
    """发布文章"""
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            cd = article_post_form.cleaned_data
            try:
                new_article = article_post_form.save(commit=False)
                new_article.author = request.user
                new_article.column = request.user.article_column.get(id=request.POST['column_id'])
                # 作者自己 创建的栏目
                new_article.save()
                return HttpResponse("1")
            except:
                return HttpResponse("2")
        else:
            return HttpResponse("3")
    else:
        article_post_form = ArticlePostForm()
        article_columns = request.user.article_column.all()
        # 作者自己创建的栏目  article_column 在ArticleColumn模型类中 related_name 属性的作用
        return render(request,"article/column/article_post.html",
                      {"article_post_form": article_post_form,"article_columns": article_columns})


@login_required(login_url="/account/login/")
def article_list(request):
    """文章标题"""
    article_list = ArticlePost.objects.filter(author=request.user)
    # 根据查询到的文章对象article_list创建分页的实例对象，每页最多两个
    paginator = Paginator(article_list,2)
    page = request.GET.get('page')
    print(page)
    try:
        # page()是 Paginator对象的一个方法，用于得到指定页面的内容，值必须大于等于1的整数
        current_page = paginator.page(page)
        print(current_page)
        # object_list是Page对象的属性，能够得到该页所有的对象列表
        articles = current_page.object_list
    except PageNotAnInteger:  # 捕获异常请求页面数值不是整数
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:       # 请求页码数值为空，或在URL参数中没有page
        # paginator.num_pages返回的是页数，num_pages是Paginator对象的一个属性
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list
    return render(request,"article/column/article_list.html",{
        "articles":articles,"page":current_page})


@login_required(login_url="/account/login/")
def article_detail(request,id,slug):
    """文章内容页面"""
    article = get_object_or_404(ArticlePost,id=id,slug=slug)
    return render(request,"article/column/article_detail.html",{"article":article})


@login_required(login_url="/account/login/")
@require_POST
@csrf_exempt
def del_article(request):
    """删除文章"""
    article_id = request.POST["article_id"]
    try:
        article = ArticlePost.objects.get(id=article_id)
        article.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")


@login_required(login_url="/account/login/")
@csrf_exempt
def redit_article(request,article_id):
    """编辑文章"""
    if request.method == "GET":
        article_columns = request.user.article_column.all() # 用户所有的栏目
        article = ArticlePost.objects.get(id=article_id)    # 当前要编辑的文章
        this_article_form = ArticlePostForm(initial={"title":article.title})    # 初始化的文章表单
        this_article_column = article.column    # 当前文章所属的栏目
        return render(request,"article/column/redit_article.html",{
            "article":article,
            "article_columns":article_columns,
            "this_article_column":this_article_column,
            "this_article_form":this_article_form
        })
    else:
        redit_article = ArticlePost.objects.get(id=article_id)
        try:
            redit_article.column = request.user.article_column .get(id=request.POST["column_id"])
            redit_article.title = request.POST["title"]
            redit_article.body = request.POST["body"]
            redit_article.save()
            return HttpResponse("1")
        except:
            return HttpResponse("2")
