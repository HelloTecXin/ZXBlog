from django import forms
from django.core.files.base import ContentFile
from slugify import slugify
from urllib import request

from .models import Image


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title','url','description')

    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg','jpeg','png'] # 规定图片的扩展名
        extension = url.rsplit('.',1)[1].lower()  # 从得到图片的网址中分解出其扩展名
        if extension not in valid_extensions:   # 如果属于规定的扩展名，就认为提交的URL对象是一个图片
            raise forms.ValidationError('The given url does not match valid image extension.')
        return url

    def save(self,force_insert=False,force_update=False,commit=True):
        # ModelForm类中的save方法，将表单提交的数据保存到数据库
        image = super(ImageForm, self).save(commit=False)  # 执行父类ModelForm的save()方法，commit=False实例虽然被建立，但并没有保存数据
        image_url = self.cleaned_data['url']
        image_name = '{0}.{1}'.format(slugify(image.title),image_url.rsplit('.',1)[1].lower())
        response = request.urlopen(image_url)  # 以get方式访问该图片地址 ，通过该对象得到所访问URL的数据（图片的ASCII）
        image.image.save(image_name, ContentFile(response.read()),save=False) #　将上述返回的结果保存到本地，并按照约定的名称给该图片文件命名
        if commit:
            image.save()
        return image
