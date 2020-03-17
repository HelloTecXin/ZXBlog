from django import forms
from .models import ArticleColumn,ArticlePost


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
