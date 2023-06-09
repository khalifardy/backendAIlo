# Generated by Django 4.1.7 on 2023-03-24 04:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="StaffProfile",
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
                ("full_name", models.CharField(blank=True, max_length=100, null=True)),
                ("nim", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "gender",
                    models.IntegerField(
                        choices=[(1, "Pria"), (2, "Wanita")], default=2
                    ),
                ),
                (
                    "religion",
                    models.IntegerField(
                        choices=[
                            (1, "Islam"),
                            (2, "Kristen"),
                            (3, "Katolik"),
                            (4, "Hindu"),
                            (5, "Buddha"),
                            (6, "Other Religion"),
                        ],
                        default=1,
                    ),
                ),
                (
                    "status",
                    models.IntegerField(
                        choices=[
                            (1, "Active"),
                            (2, "Terminate"),
                            (3, "Resign"),
                            (4, "Other Agent Status"),
                        ],
                        default=1,
                    ),
                ),
                ("date_of_birth", models.DateField(blank=True, null=True)),
                ("date_start", models.DateTimeField(blank=True, null=True)),
                ("date_end", models.DateTimeField(blank=True, null=True)),
                ("first_login", models.BooleanField(blank=True)),
                (
                    "user",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Staff Profile",
                "verbose_name_plural": "Staff Profiles",
            },
        ),
        migrations.CreateModel(
            name="Level",
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
                (
                    "tipe",
                    models.IntegerField(
                        blank=True,
                        choices=[
                            (1, "Direktur"),
                            (2, "Wakil Direktur"),
                            (3, "Koordinator Asisten"),
                            (4, "Kepala Dvisi"),
                            (5, "Staff"),
                        ],
                        default=5,
                        null=True,
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Level",
                "verbose_name_plural": "Staff Level",
            },
        ),
        migrations.CreateModel(
            name="AdminRole",
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
                ("admin", models.BooleanField(default=False)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Admin Role",
                "verbose_name_plural": "Admin Roles",
            },
        ),
    ]
