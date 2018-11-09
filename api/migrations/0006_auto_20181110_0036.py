# Generated by Django 2.1.3 on 2018-11-09 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20181110_0034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='comments',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivered_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='scheduled_deliver_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='comments',
            field=models.TextField(null=True),
        ),
    ]
