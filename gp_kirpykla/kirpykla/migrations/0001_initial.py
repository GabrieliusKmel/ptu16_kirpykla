# Generated by Django 4.2.6 on 2023-10-16 11:14

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('price', models.DecimalField(decimal_places=2, max_digits=18, verbose_name='price')),
                ('duration', models.DurationField(default=datetime.timedelta(seconds=1800), verbose_name='duration')),
                ('about', tinymce.models.HTMLField(blank=True, default='', max_length=10000, verbose_name='about')),
            ],
            options={
                'verbose_name': 'service',
                'verbose_name_plural': 'services',
            },
        ),
        migrations.CreateModel(
            name='ServiceOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'confirmed'), (1, 'completed'), (2, 'cancelled')], default=0, verbose_name='status')),
                ('service_time', models.DateTimeField(blank=True, null=True, verbose_name='service_time')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('barber', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to=settings.AUTH_USER_MODEL, verbose_name='barber')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_orders', to=settings.AUTH_USER_MODEL, verbose_name='customer')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kirpykla.service', verbose_name='service')),
            ],
            options={
                'verbose_name': 'serviceorder',
                'verbose_name_plural': 'serviceorders',
            },
        ),
        migrations.CreateModel(
            name='BarberReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=4000, verbose_name='content')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('barber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_reviews', to=settings.AUTH_USER_MODEL, verbose_name='barber')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='barber_reviews', to=settings.AUTH_USER_MODEL, verbose_name='reviewer')),
            ],
            options={
                'verbose_name': 'barberreview',
                'verbose_name_plural': 'barberreviews',
            },
        ),
    ]
