# Generated by Django 5.1.5 on 2025-02-19 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0022_alter_game_jam_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='images',
            field=models.ImageField(blank=True, upload_to='uploads/'),
        ),
        migrations.AlterField(
            model_name='dev_log',
            name='images',
            field=models.ImageField(blank=True, upload_to='uploads/'),
        ),
        migrations.AlterField(
            model_name='thread',
            name='images',
            field=models.ImageField(blank=True, upload_to='uploads/'),
        ),
    ]
