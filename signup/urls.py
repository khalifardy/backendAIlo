from django.urls import re_path, include
from .views import Signup, Search, AdminSignup, Login, UploadFotoProfile, ListSignUpAdmin

urlpatterns = [
    re_path(r'^staff/$', Signup.as_view(), name='signup'),
    re_path(r'^search/$', Search.as_view(), name='search'),
    re_path(r'^admin/$', AdminSignup.as_view(), name='adminsignup'),
    re_path(r'^login/$', Login.as_view(), name='login'),
    re_path(r'^upload_foto_profile/$',
            UploadFotoProfile.as_view(), name='upload'),
    re_path(r'^edit_status/$',
            ListSignUpAdmin.as_view(), name='edit_status'),


]
