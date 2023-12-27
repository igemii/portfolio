# Generated by Django 5.0 on 2023-12-18 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to='post_images/'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='profile_images/'),
        ),
    ]