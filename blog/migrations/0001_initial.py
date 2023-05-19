# Generated by Django 4.1.7 on 2023-04-14 21:01

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Artikel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                ("label", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "judul",
                    models.CharField(
                        blank=True, default="Untitled", max_length=100, null=True
                    ),
                ),
                ("konten", models.TextField(blank=True, default="", null=True)),
                ("author", models.CharField(max_length=100)),
                ("kategori", models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                "verbose_name": "Artikel",
                "verbose_name_plural": "Artikel",
            },
        ),
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                ("urutan", models.IntegerField(blank=True, default=None, null=True)),
                (
                    "artikel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="blog.artikel"
                    ),
                ),
            ],
            options={
                "verbose_name": "Artikel",
                "verbose_name_plural": "Artikel",
            },
        ),
    ]