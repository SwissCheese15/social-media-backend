# Generated by Django 4.1.1 on 2022-10-07 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='Title',
            new_name='title',
        ),
        migrations.AddField(
            model_name='post',
            name='content',
            field=models.TextField(blank=True, max_length=500),
        ),
    ]
