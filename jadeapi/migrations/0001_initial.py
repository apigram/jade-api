# Generated by Django 2.1.3 on 2018-11-08 06:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('business_number', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CompanyContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('role', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100)),
                ('quantity', models.IntegerField()),
                ('unit_price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('received_date', models.DateTimeField()),
                ('scheduled_deliver_date', models.DateTimeField()),
                ('delivered_date', models.DateTimeField()),
                ('status', models.CharField(max_length=100)),
                ('comments', models.TextField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client_order', to='jadeapi.Company')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('price', models.FloatField()),
                ('comments', models.TextField()),
                ('items', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jadeapi.Item')),
                ('orders', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jadeapi.Order')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=1000)),
                ('contact', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='jadeapi.Contact')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(through='jadeapi.OrderItem', to='jadeapi.Item'),
        ),
        migrations.AddField(
            model_name='order',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supplier_order', to='jadeapi.Company'),
        ),
        migrations.AddField(
            model_name='companycontact',
            name='contact',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='jadeapi.Contact'),
        ),
        migrations.AddField(
            model_name='company',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jadeapi.CompanyContact'),
        ),
        migrations.AddField(
            model_name='company',
            name='suppliers',
            field=models.ManyToManyField(related_name='_company_suppliers_+', to='jadeapi.Company'),
        ),
    ]
