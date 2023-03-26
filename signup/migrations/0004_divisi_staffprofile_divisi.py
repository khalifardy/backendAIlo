# Generated by Django 4.1.7 on 2023-03-26 05:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("signup", "0003_alter_staffprofile_first_login"),
    ]

    operations = [
        migrations.CreateModel(
            name="Divisi",
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
                ("nama_divisi", models.CharField(max_length=100)),
            ],
            options={
                "verbose_name": "Divisi",
                "verbose_name_plural": "Divisi",
            },
        ),
        migrations.AddField(
            model_name="staffprofile",
            name="divisi",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="signup.divisi",
            ),
        ),
    ]