# Generated by Django 2.1.3 on 2018-11-09 13:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_company_suppliers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='received_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
