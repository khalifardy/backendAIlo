from django.shortcuts import render
from django.contrib.auth.models import User
#from django.db.models import Q sebuah nama 

#library django-rest-framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

#library python
import datetime

#library internal
from libint import KonversiChoice
#models
from .models import StaffProfile,Level,AdminRole,Divisi

#serializers
from .serializers import StaffProfileSerializer
# Create your views here.

class Signup(APIView):
    """
    Kelas untuk signup staff
    """

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
        divisi = data.get('divisi',None)

        konversi = KonversiChoice()
        date_of_birth = datetime.datetime.strptime(date_of_birth, '%Y-%m-%d')

        if not username or not password or not email or not gender or not religion or not first_name or not last_name or not fullname or not date_of_birth or not nim:
            return Response({"msg":"Please fill all fields"},status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists():
            return Response({"msg":"Username Sudah Ada"},status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({"msg":"Email Sudah Ada"},status=status.HTTP_400_BAD_REQUEST)
        if StaffProfile.objects.filter(nim=nim).exists():
            return Response({"msg":"User Sudah Ada"},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            User.objects.create_user(username=username, password=password, email=email)
            
            if divisi:
                divisi = Divisi.objects.get(nama_divisi=divisi)
                StaffProfile.objects.create(user=User.objects.get(username=username),gender=konversi.gender(gender),
                                        religion=konversi.religion(religion),
                                        full_name=fullname,
                                        date_of_birth=date_of_birth, nim=nim, divisi=divisi)
            else:
                StaffProfile.objects.create(user=User.objects.get(username=username),gender=konversi.gender(gender),
                                            religion=konversi.religion(religion),
                                            full_name=fullname,
                                            date_of_birth=date_of_birth, nim=nim)
            
        except Exception as e:
            return Response({"msg":str(e)},status=status.HTTP_400_BAD_REQUEST)
        return Response({"msg":"Sukses membuat"},status=status.HTTP_201_CREATED)

class Search(APIView):
    """
    Kelas untuk Search Staff
    """

    def post(self, request):
        nama = request.data.get('nama',None)
        nim = request.data.get('nim',None)

        if nama and nim:
            staff = StaffProfile.objects.filter(nim=nim,full_name__icontains=nama)
        elif nama:
            staff = StaffProfile.objects.filter(full_name__icontains=nama)
        elif nim:
            staff = StaffProfile.objects.filter(nim=nim)
        else:
            staff = StaffProfile.objects.all()
            
        serializer = StaffProfileSerializer(staff, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class AdminSignup(APIView):

    def get(self,request):
        nama = request.GET.get('nama',None)
        nim = request.GET.get('nim',None)

        if nama and nim:
            staff = StaffProfile.objects.filter(nim=nim,full_name__icontains=nama)
        elif nama:
            staff = StaffProfile.objects.filter(full_name__icontains=nama)
        elif nim:
            staff = StaffProfile.objects.filter(nim=nim)
        else:
            staff = StaffProfile.objects.all()
            
        serializer = StaffProfileSerializer(staff, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
        

    def post(self, request):
        admin = request.user.adminrole

        if not admin:
            return Response({"msg":"Anda Bukan Admin"},status=status.HTTP_404)
        
        konver = KonversiChoice()
        nim = request.data.get('nim')
        status = request.data.get('status')
        level = request.data.get('level')

        query = StaffProfile.objects.get(nim=nim)

        try:
            query.update_status(status=konver.status(status))
        except Exception as e:
            return Response({"msg":str(e)},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(username=query.user.username)
            Level.objects.create(user=user,level=konver.level(level))
            query.update_status(user=user,status=konver.status(status))
        except Exception as e:
            return Response({"msg":str(e)},status=status.HTTP_400_BAD_REQUEST)
        
        
        return Response({"msg":"Sukses Mengubah Status"},status=status.HTTP_200_OK)
    






