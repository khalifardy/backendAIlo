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

# serializers
from .serializers import ArtikelSerializer


class UploadArtikel(APIView):
    permission_classes = (IsTokenValid,)

    def post(self, request, format=None):
        image = request.FILES.getlist('image', None)
        judul = request.data.get('judul', None)
        konten = request.data.get('konten', None)
        label = request.data.get('label', None)
        kategori = request.data.get('kategori', None)
        author = request.user.staffprofile.full_name

        path = settings.MEDIA_ROOT + 'blog/images'

        if not os.path.isdir(path):
            os.makedirs(path)

        try:
            id_kategori = Kategori.objects.get(name=kategori)
            print(id_kategori)
            Artikel.objects.create(
                judul=judul,
                konten=konten,
                label=label,
                kategori=id_kategori,
                author=author,
            )

            id_artikel = Artikel.objects.last().id
            objek_artikel = Artikel.objects.get(id=id_artikel)
            if image:
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


class BlogView(APIView):
    permission_classes = (IsTokenValid,)

    def get(self, request):
        id_artikel = request.data.get('id', None)
        admin = request.user.adminrole.admin
        author = request.user.staffprofile.full_name

        if admin:
            artikel = Artikel.objects.all()
        else:
            artikel = Artikel.objects.filter(author=author)

        if id_artikel:
            artikel = artikel.filter(id=id_artikel)

        serial = ArtikelSerializer(artikel, many=True)

        return Response(data=serial.data, status=status.HTTP_200_OK)

    def post(self, request):
        id_artikel = request.data.get('id_artikel')
        id_images = request.data.getlist('id_images', None)
        images = request.FILES.getlist('images', None)
        judul = request.data.get('judul', None)
        konten = request.data.get('konten', None)
        label = request.data.get('label', None)
        kategori = request.data.get('kategori', None)

        try:
            obj = Artikel.objects.get(id=id_artikel)
            path = settings.MEDIA_ROOT + 'blog/images'

            if judul:
                obj.judul = judul

            if konten:
                obj.konten = konten

            if label:
                obj.label = label

            if kategori:
                kategori_obj = Kategori.objects.get(name=kategori)
                obj.kategori = kategori_obj

            if len(id_images) > 0:
                id_images = [int(i) for i in id_images]
                print(id_images)
                print(images)
                for i in range(len(images)):
                    Upload_path = os.path.join(
                        path, judul+"_"+images[i].name)
                    with open(Upload_path, 'wb+') as destination:
                        for chunk in images[i].chunks():
                            destination.write(chunk)

                    obj_images = Image.objects.get(id=id_images[i])
                    obj_images.url = Upload_path
                    obj_images.save()

            respon = {
                "msg": "Update Berhasil",
                "status": status.HTTP_202_ACCEPTED
            }

            obj.save()
        except Exception as e:
            respon = {
                "msg": str(e),
                "status": status.HTTP_400_BAD_REQUEST
            }

        return Response(respon)
