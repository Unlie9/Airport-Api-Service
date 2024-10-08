# Generated by Django 5.0.8 on 2024-08-11 20:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AirplaneType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
            ],
            options={
                'verbose_name_plural': 'AirplaneTypes',
            },
        ),
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('closest_big_city', models.CharField(max_length=64)),
            ],
            options={
                'verbose_name_plural': 'Airports',
            },
        ),
        migrations.CreateModel(
            name='Crew',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
            ],
            options={
                'verbose_name_plural': 'Crews',
            },
        ),
        migrations.CreateModel(
            name='Airplane',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('rows', models.IntegerField()),
                ('seats_in_row', models.IntegerField()),
                ('airplane_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='airport.airplanetype')),
            ],
            options={
                'verbose_name_plural': 'Airplanes',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distance', models.IntegerField()),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arrival_routes', to='airport.airport')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departure_routes', to='airport.airport')),
            ],
            options={
                'verbose_name_plural': 'Routes',
            },
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure_time', models.DateTimeField()),
                ('arrival_time', models.DateTimeField()),
                ('airplane', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='airport.airplane')),
                ('crew', models.ManyToManyField(to='airport.crew')),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='airport.route')),
            ],
            options={
                'verbose_name_plural': 'Flights',
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row', models.IntegerField()),
                ('seat', models.IntegerField()),
                ('flight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='airport.flight')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='airport.order')),
            ],
            options={
                'verbose_name_plural': 'Tickets',
                'ordering': ['seat'],
            },
        ),
        migrations.AddIndex(
            model_name='route',
            index=models.Index(fields=['source', 'destination'], name='airport_rou_source__5c8f4c_idx'),
        ),
        migrations.AddIndex(
            model_name='route',
            index=models.Index(fields=['distance'], name='airport_rou_distanc_e43817_idx'),
        ),
        migrations.AddIndex(
            model_name='flight',
            index=models.Index(fields=['route', 'airplane'], name='airport_fli_route_i_6c5c8a_idx'),
        ),
        migrations.AddIndex(
            model_name='flight',
            index=models.Index(fields=['departure_time'], name='airport_fli_departu_abe547_idx'),
        ),
        migrations.AddIndex(
            model_name='flight',
            index=models.Index(fields=['arrival_time'], name='airport_fli_arrival_a12903_idx'),
        ),
        migrations.AddConstraint(
            model_name='ticket',
            constraint=models.UniqueConstraint(fields=('row', 'seat', 'flight'), name='unique_ticket_seat_row_flight'),
        ),
    ]
