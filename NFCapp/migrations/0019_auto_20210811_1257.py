# Generated by Django 3.2.4 on 2021-08-11 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NFCapp', '0018_auto_20210810_2109'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainer',
            name='password',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='trainer',
            name='username',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
