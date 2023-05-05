from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.conf import settings

# library django-rest-framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_jwt.settings import api_settings
# library python
from datetime import datetime
import os

# library internal
from libint import IsTokenValid

# models
from .models import Artikel, Image, Kategori


class UploadArtikel(APIView):
    permission_classes = (IsTokenValid,)

    def post(self, request, format=None):
        image = request.FILES.getlist('image')
        judul = request.data.get('judul', None)
        konten = request.data.get('konten', None)
        label = request.data.get('label', None)
        kategori = request.data.get('kategori', None)
        author = request.user.staffprofile.full_name

        path = settings.MEDIA_ROOT + 'blog/images'

        if not os.path.isdir(path):
            os.makedirs(path)

        try:
            id_kategori = Kategori.objects.get(name=kategori).id
            Artikel.objects.create(
                judul=judul,
                konten=konten,
                label=label,
                kategori=id_kategori,
                author=author,
            )

            id_artikel = Artikel.objects.last().id
            objek_artikel = Artikel.objects.get(id=id_artikel)
            for i, file_obj in enumerate(image):
                Upload_path = os.path.join(
                    path, judul+"_"+file_obj.name)
                with open(Upload_path, 'wb+') as destination:
                    for chunk in file_obj.chunks():
                        destination.write(chunk)
                Image.objects.create(
                    artikel=objek_artikel,
                    url=Upload_path,
                    urutan=i+1
                )
            return Response({'msg': 'Konten Behasil di Posting'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)
