# Generated by Django 2.1.3 on 2018-11-09 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20181110_0020'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='suppliers',
        ),
    ]
