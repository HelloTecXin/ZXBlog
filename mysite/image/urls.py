from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'image'

urlpatterns = [
    path('list-images/',views.list_images,name='list_images'),
    path('upload-image/',views.upload_image, name='upload_image'),
    path('del-image/',views.del_image,name='del_image'),
    path('images/',views.falls_images,name='falls_images'),


]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
