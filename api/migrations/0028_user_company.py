# Generated by Django 2.1.2 on 2019-06-27 00:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_auto_20190405_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='company',
            field=models.OneToOneField(default=6, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='api.Company'),
            preserve_default=False,
        ),
    ]