# Generated by Django 3.1.7 on 2021-04-10 18:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_auto_20210410_1814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='follower',
            field=models.ManyToManyField(blank=True, related_name='folower', to=settings.AUTH_USER_MODEL),
        ),
    ]
