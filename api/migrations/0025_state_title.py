# Generated by Django 2.1.2 on 2019-04-05 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='state',
            name='title',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]