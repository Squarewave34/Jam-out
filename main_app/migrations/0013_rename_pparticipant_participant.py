# Generated by Django 5.1.5 on 2025-02-16 17:31

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0012_rename_participants_pparticipant'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='pParticipant',
            new_name='Participant',
        ),
    ]
