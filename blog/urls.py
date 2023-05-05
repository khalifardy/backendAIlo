from django.urls import re_path, include
from .views import UploadArtikel

urlpatterns = [
    re_path(r'^upload/$', UploadArtikel.as_view(), name='posting'),
]
