# Generated by Django 3.2.4 on 2021-08-02 15:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('NFCapp', '0014_alter_galleryimage_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField()),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profile_pic/')),
                ('facebook_url', models.CharField(max_length=255, null=True)),
                ('twitter_url', models.CharField(max_length=255, null=True)),
                ('instgram_url', models.CharField(max_length=255, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
