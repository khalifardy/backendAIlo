# third party
from rest_framework import serializers

# models
from .models import Artikel, Image

# libray python
from datetime import datetime


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "url", "urutan"]


class ArtikelSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    kategori = serializers.SerializerMethodField(method_name="get_kategori")
    modified = serializers.SerializerMethodField(method_name="get_modified")

    class Meta:
        model = Artikel
        fields = ["modified", "id", "label", "judul",
                  "konten", "author", "kategori", "images"]

    def get_kategori(self, obj):
        try:
            return obj.kategori.name
        except:
            return "-"

    def get_modified(self, obj):
        return obj.modified.strftime("%d-%m-%Y")
