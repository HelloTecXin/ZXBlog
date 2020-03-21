from django import forms
from .models import ArticleColumn,ArticlePost,Comment
from .models import ArticleTag


class ArticleColumnForm(forms.ModelForm):
    """栏目表单"""
    class Meta:
        model = ArticleColumn
        fields= ("column",)


class ArticlePostForm(forms.ModelForm):
    """文章表单"""
    class Meta:
        model = ArticlePost
        fields = ("title","body")


class CommentForm(forms.ModelForm):
    """评论表单"""
    class Meta:
        model = Comment
        fields = ("commentator","body",)


class ArticleTagForm(forms.ModelForm):
    """标签表单"""
    class Meta:
        model = ArticleTag
        fields=("tag",)