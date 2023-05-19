from django.urls import re_path, include
from .views import UploadArtikel, BlogView

urlpatterns = [
    re_path(r'^upload/$', UploadArtikel.as_view(), name='posting'),
    re_path(r'^dataget/$', BlogView.as_view(), name='data'),
]
