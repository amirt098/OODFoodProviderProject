# Generated by Django 5.0.6 on 2024-08-05 01:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('logistic', '0001_initial'),
        ('provider', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Record Created on specific date time', verbose_name='Created')),
                ('modified', models.DateTimeField(auto_now=True, help_text='Record Modified on specific date time', verbose_name='Modified')),
                ('uid', models.CharField(max_length=255, unique=True, verbose_name='Order UID')),
                ('state', models.CharField(choices=[('W', 'Waiting for payment'), ('E', 'Expired payment'), ('C', 'Cancelled'), ('P', 'Processing'), ('S', 'Shipped'), ('D', 'Delivered')], default='W', max_length=1, verbose_name='Status')),
                ('footnote', models.TextField(blank=True, help_text='any additional info needed by admins', null=True, verbose_name='Footnote')),
                ('driver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='logistic.driver', verbose_name='Driver')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='provider.provider', verbose_name='Provider')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='accounts.user', verbose_name='User')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1, verbose_name='Quantity')),
                ('price', models.PositiveBigIntegerField(verbose_name='Sell Price')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='order.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='provider.product')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(related_name='orders', through='order.OrderItem', to='provider.product', verbose_name='Products'),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Record Created on specific date time', verbose_name='Created')),
                ('modified', models.DateTimeField(auto_now=True, help_text='Record Modified on specific date time', verbose_name='Modified')),
                ('uid', models.CharField(max_length=255, unique=True, verbose_name='Review UID')),
                ('rating', models.PositiveSmallIntegerField(verbose_name='Rating')),
                ('message', models.CharField(max_length=300, verbose_name='Message')),
                ('driver_rating', models.PositiveSmallIntegerField(verbose_name='Driver rating')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='order.order', verbose_name='order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='accounts.user', verbose_name='User')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
