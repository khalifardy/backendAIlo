#third party
from rest_framework import serializers

#models
from.models import Level,StaffProfile



class LevelSerializer(serializers.ModelSerializer):
    
    tipe = serializers.SerializerMethodField()
    class Meta:
        model = Level
        fields = ["tipe"]
    
    def get_tipe(self, obj):
        return obj.get_tipe_display()

class StaffProfileSerializer(serializers.ModelSerializer):

    gender = serializers.SerializerMethodField()
    religion = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()
    divisi = serializers.SerializerMethodField()
    class Meta:
        model = StaffProfile
        fields = ["full_name","nim","gender", "religion", "status","date_of_birth","level","divisi"]

    def get_gender(self, obj):
        return obj.get_gender_display()
    
    def get_religion(self, obj):
        return obj.get_religion_display()
    
    def get_status(self, obj):
        return obj.get_status_display()
    
    def get_level(self, obj):
        return obj.user.level.get_tipe_display()
    
    def get_divisi(self, obj):
        return obj.divisi.nama_divisi
    