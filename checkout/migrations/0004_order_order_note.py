# Generated by Django 3.2.13 on 2022-05-31 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0003_alter_order_expected_done_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_note',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]
