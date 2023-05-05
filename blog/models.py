from django.db import models
from django.contrib.auth.models import User

# third party imports
from django_extensions.db.models import TimeStampedModel


class Kategori(TimeStampedModel):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = 'blog'
        verbose_name = 'Kategori'
        verbose_name_plural = 'Kategori'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Artikel(TimeStampedModel):
    label = models.CharField(max_length=100, blank=True, null=True)
    judul = models.CharField(max_length=100, blank=True,
                             null=True, default="Untitled")
    konten = models.TextField(blank=True, null=True, default="")
    author = models.CharField(max_length=100)
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE)

    class Meta:
        app_label = 'blog'
        verbose_name = 'Artikel'
        verbose_name_plural = 'Artikel'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return self.judul


class Image(TimeStampedModel):
    artikel = models.ForeignKey(Artikel, on_delete=models.CASCADE)
    url = models.CharField(max_length=100, blank=True, null=True)
    urutan = models.IntegerField(blank=True, null=True, default=None)

    class Meta:
        app_label = 'blog'
        verbose_name = 'Artikel'
        verbose_name_plural = 'Artikel'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
