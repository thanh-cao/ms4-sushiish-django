# Generated by Django 3.2.13 on 2022-06-05 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_rename_user_id_userprofile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
