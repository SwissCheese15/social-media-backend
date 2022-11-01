# Generated by Django 4.1.1 on 2022-10-09 12:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_following',
            field=models.ManyToManyField(blank=True, default=None, related_name='is_followed_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
