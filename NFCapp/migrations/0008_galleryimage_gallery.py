# Generated by Django 3.2.4 on 2021-07-29 04:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('NFCapp', '0007_gallery_galleryimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='galleryimage',
            name='Gallery',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='NFCapp.gallery'),
        ),
    ]
