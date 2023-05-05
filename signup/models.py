from django.db import models
from django.contrib.auth.models import User

# third party imports
from django_extensions.db.models import TimeStampedModel
# Create your models here.


class ProfileImage(models.Model):
    url = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        app_label = 'signup'
        verbose_name = 'Profile Image'
        verbose_name_plural = 'Profile Image'


class Level(TimeStampedModel):
    DIREKTUR = 1
    WAKIL_DIREKTUR = 2
    KOORDINATOR_ASISTEN = 3
    KEPALA_DIVISI = 4
    STAFF = 5

    LEVELS = [
        (DIREKTUR, 'Direktur'),
        (WAKIL_DIREKTUR, 'Wakil Direktur'),
        (KOORDINATOR_ASISTEN, 'Koordinator Asisten'),
        (KEPALA_DIVISI, 'Kepala Dvisi'),
        (STAFF, 'Staff'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipe = models.IntegerField(
        choices=LEVELS, default=STAFF, blank=True, null=True)

    class Meta:
        app_label = 'signup'
        verbose_name = 'Level'
        verbose_name_plural = 'Staff Level'

    def __init__(self, *args: any, **kwargs: any) -> None:
        super().__init__(*args, **kwargs)

    def __unicode__(self):
        return "Staff Level untuk %s" % self.user.username


class Divisi(models.Model):

    nama_divisi = models.CharField(max_length=100)

    class Meta:
        app_label = 'signup'
        verbose_name = 'Divisi'
        verbose_name_plural = 'Divisi'


class StaffProfile(TimeStampedModel):
    PRIA = 1
    WANITA = 2

    GENDER_CHOICES = (
        (PRIA, 'Pria'),
        (WANITA, 'Wanita'),
    )

    ISLAM = 1
    KRISTEN = 2
    KATHOLIK = 3
    HINDU = 4
    BUDDHA = 5
    OTHER_RELIGION = 6
    RELIGION_CHOICES = (
        (ISLAM, 'Islam'),
        (KRISTEN, 'Kristen'),
        (KATHOLIK, 'Katolik'),
        (HINDU, 'Hindu'),
        (BUDDHA, 'Buddha'),
        (OTHER_RELIGION, 'Other Religion'),
    )

    ACTIVE = 1
    TERMINATE = 2
    RESIGN = 3
    ALUMNI = 4
    OTHER_STAFF_STATUS = 5
    STAFF_STATUSES = (
        (ACTIVE, 'Active'),
        (TERMINATE, 'Terminate'),
        (RESIGN, 'Resign'),
        (ALUMNI, 'Alumni'),
        (OTHER_STAFF_STATUS, 'Other STAFF Status'),
    )

    user = models.OneToOneField(
        User, blank=True, null=True, on_delete=models.CASCADE)
    full_name = models.CharField(blank=True, null=True, max_length=100)
    nim = models.CharField(blank=True, null=True, max_length=100)
    gender = models.IntegerField(choices=GENDER_CHOICES, default=WANITA)
    religion = models.IntegerField(choices=RELIGION_CHOICES, default=ISLAM)
    status = models.IntegerField(choices=STAFF_STATUSES, default=ACTIVE)
    date_of_birth = models.DateField(blank=True, null=True)
    date_start = models.DateTimeField(blank=True, null=True)
    date_end = models.DateTimeField(blank=True, null=True)
    first_login = models.BooleanField(blank=True, null=True)
    divisi = models.ForeignKey(
        Divisi, blank=True, null=True, on_delete=models.CASCADE)
    foto = models.ForeignKey(ProfileImage, on_delete=models.CASCADE,
                             blank=True, null=True)

    class Meta:
        app_label = 'signup'
        verbose_name = 'Staff Profile'
        verbose_name_plural = 'Staff Profiles'

    def __init__(self, *args, **kwargs):
        super(StaffProfile, self).__init__(*args, **kwargs)

    def __unicode__(self):
        if self.user is not None:
            name = self.user.username
        else:
            name = self.nim

        return "Staff Profile for %s" % name


class InfoDirektur(models.Model):
    appresiasi = models.CharField(max_length=100, null=True, blank=True)
    spesialisasi = models.CharField(max_length=100, null=True, blank=True)
    person = models.ForeignKey(StaffProfile, on_delete=models.CASCADE)


class AdminRole(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    admin = models.BooleanField(default=False)

    class Meta:
        app_label = 'signup'
        verbose_name = 'Admin Role'
        verbose_name_plural = 'Admin Roles'


class MediaSosial(models.Model):
    nama_media = models.CharField(max_length=100)

    class Meta:
        app_label = 'signup'
        verbose_name = 'Media Sosial'
        verbose_name_plural = 'Media Sosial'


class StaffMedia(models.Model):
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE)
    medsos = models.ForeignKey(MediaSosial, on_delete=models.CASCADE)
    akun = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        app_label = 'signup'
        verbose_name = 'StaffMedia'
        verbose_name_plural = 'StaffMedia'
