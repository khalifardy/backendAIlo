from django.urls import re_path,include
from .views import Signup,Search

urlpatterns = [
    re_path(r'^staff/$', Signup.as_view(), name='signup'),
    re_path(r'^search/$', Search.as_view(), name='search'),
]