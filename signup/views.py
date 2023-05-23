from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.conf import settings
# from AILO import settings
# from django.db.models import Q sebuah nama

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
from libint import KonversiChoice, IsTokenValid
# models
from .models import StaffProfile, Level, Divisi, AdminRole, ProfileImage

# serializers
from .serializers import StaffProfileSerializer
# Create your views here.


class Signup(APIView):
    """
    Kelas untuk signup staff, cek
    """
    permission_classes = (AllowAny,)

    def get(self, request):
        query_divisi = Divisi.objects.all()
        gender = ["PRIA", "WANITA"]
        religion = ["ISLAM", "KRISTEN", "KATHOLIK",
                    "HINDU", "BUDDHA", "OTHER_RELIGION"]
        divisi = [i.nama_divisi for i in query_divisi]

        respon = {
            "gender": gender,
            "religion": religion,
            "divisi": divisi,

        }

        return Response(respon, status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        gender = data.get('gender')
        religion = data.get('religion')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        fullname = first_name + ' ' + last_name
        date_of_birth = data.get('date_of_birth')
        nim = data.get('nim')
        divisi = data.get('divisi', None)

        konversi = KonversiChoice()
        date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d')

        if not username or not password or not email or not gender or not religion or not first_name or not last_name or not fullname or not date_of_birth or not nim:
            return Response({"msg": "Please fill all fields"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"msg": "Username Sudah Ada"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({"msg": "Email Sudah Ada"}, status=status.HTTP_400_BAD_REQUEST)
        if StaffProfile.objects.filter(nim=nim).exists():
            return Response({"msg": "User Sudah Ada"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            User.objects.create_user(
                username=username, password=password, email=email)

            if divisi:
                divisi = Divisi.objects.get(nama_divisi=divisi)
                StaffProfile.objects.create(user=User.objects.get(username=username), gender=konversi.gender(gender),
                                            religion=konversi.religion(
                                                religion),
                                            full_name=fullname,
                                            date_of_birth=date_of_birth, nim=nim, divisi=divisi)
            else:
                StaffProfile.objects.create(user=User.objects.get(username=username), gender=konversi.gender(gender),
                                            religion=konversi.religion(
                                                religion),
                                            full_name=fullname,
                                            date_of_birth=date_of_birth, nim=nim)

            AdminRole.objects.create(user=User.objects.get(username=username))

        except Exception as e:
            return Response({"msg": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"msg": "Sukses membuat"}, status=status.HTTP_201_CREATED)


class Search(APIView):
    """
    Kelas untuk Search Staff
    """
    permission_classes = (IsTokenValid,)

    def post(self, request):
        nama = request.data.get('nama', None)
        nim = request.data.get('nim', None)

        if nama and nim:
            staff = StaffProfile.objects.filter(
                nim=nim, full_name__icontains=nama)
        elif nama:
            staff = StaffProfile.objects.filter(full_name__icontains=nama)
        elif nim:
            staff = StaffProfile.objects.filter(nim=nim)
        else:
            staff = StaffProfile.objects.all()

        serializer = StaffProfileSerializer(staff, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class AdminSignup(APIView):

    permission_classes = [IsTokenValid,]

    def get(self, request):
        nama = request.GET.get('nama', None)
        nim = request.GET.get('nim', None)

        if nama and nim:
            staff = StaffProfile.objects.filter(
                nim=nim, full_name__icontains=nama)
        elif nama:
            staff = StaffProfile.objects.filter(full_name__icontains=nama)
        elif nim:
            staff = StaffProfile.objects.filter(nim=nim)
        else:
            staff = StaffProfile.objects.all()

        serializer = StaffProfileSerializer(staff, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        admin = request.user.adminrole.admin

        if not admin:
            return Response({"msg": "Anda Bukan Admin"}, status=status.HTTP_400_BAD_REQUEST)

        konver = KonversiChoice()
        nim = request.data.get('nim')

        stat = request.data.get('status')
        level = request.data.get('level')

        query = StaffProfile.objects.get(nim=nim)

        try:
            query.status = konver.status(stat)
            query.save()
        except Exception as e:
            return Response({"msg": str(e)})

        try:
            if (not Level.objects.filter(user=query.user).exists()):
                Level.objects.create(
                    user=query.user, tipe=konver.levels(level))
            else:
                level_staff = Level.objects.filter(user=query.user)

                level_staff.update(tipe=konver.levels(level))

        except Exception as e:
            return Response({"msg": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"msg": "Sukses Mengubah Status"}, status=status.HTTP_200_OK)


class Login(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            try:
                role = Level.objects.get(user=user).tipe
            except:
                role = "-"

            msg = {'role': role, 'token': token}

            return Response(msg, status=status.HTTP_200_OK)
        else:
            return Response({"msg": "Username atau Password Salah"}, status=status.HTTP_400_BAD_REQUEST)


class UploadFotoProfile(APIView):
    permission_classes = (IsTokenValid,)

    def post(self, request):
        img = request.FILES.get('img')
        usr = request.user.staffprofile

        path = settings.MEDIA_ROOT + 'signup/images'

        if not os.path.exists(path):
            os.makedirs(path)

        try:
            upload_path = os.path.join(
                path, "image_"+usr.full_name+".jpg"
            )

            with open(upload_path, 'wb+') as destination:
                for chunk in img.chunks():
                    destination.write(chunk)
            ProfileImage.objects.create(
                url=upload_path
            )

            last_image = ProfileImage.objects.last().id
            StaffProfile.objects.filter(nim=usr.nim).update(foto=last_image)

            return Response({"msg": "Sukses Mengubah Foto"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"msg": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ListSignUpAdmin(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        query_divisi = Divisi.objects.all()
        gender = ["PRIA", "WANITA"]
        religion = ["ISLAM", "KRISTEN", "KATHOLIK",
                    "HINDU", "BUDDHA", "OTHER_RELIGION"]
        divisi = [i.nama_divisi for i in query_divisi]
        level = ["DIREKTUR", "WADIR", "KOORDAS", "KADIV", "STAFF"]
        stat = ["ACTIVE", "TERMINATE", "RESIGN",
                "ALUMNI", "OTHER_STAFF_STATUS"]

        respon = {
            "level": level,
            "gender": gender,
            "religion": religion,
            "divisi": divisi,
            "status": stat

        }

        return Response(respon, status.HTTP_200_OK)
