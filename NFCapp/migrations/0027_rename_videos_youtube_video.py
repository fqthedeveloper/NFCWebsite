# Generated by Django 3.2.7 on 2021-10-09 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('NFCapp', '0026_youtube'),
    ]

    operations = [
        migrations.RenameField(
            model_name='youtube',
            old_name='videos',
            new_name='video',
        ),
    ]