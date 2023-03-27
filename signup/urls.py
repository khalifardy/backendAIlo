from django.urls import re_path,include
from .views import Signup,Search,AdminSignup

urlpatterns = [
    re_path(r'^staff/$', Signup.as_view(), name='signup'),
    re_path(r'^search/$', Search.as_view(), name='search'),
    re_path(r'^admin/$', AdminSignup.as_view(), name='adminsignup'),
]