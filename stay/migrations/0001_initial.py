# Generated by Django 2.1 on 2019-07-09 16:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('staying', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('parent_comment_id', models.IntegerField(default=0)),
                ('evaluation_items1', models.IntegerField(default=5)),
                ('evaluation_items2', models.IntegerField(default=5)),
                ('evaluation_items3', models.IntegerField(default=5)),
                ('evaluation_items4', models.IntegerField(default=5)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='room_image/%Y/%m/%d')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booker', models.CharField(max_length=20)),
                ('phone_number', models.CharField(max_length=30)),
                ('check_in', models.DateTimeField()),
                ('check_out', models.DateTimeField()),
                ('check_hours', models.BooleanField(default=False)),
                ('check_days', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('hours_available', models.IntegerField(default=0)),
                ('days_check_in', models.IntegerField(default=0)),
                ('days_check_out', models.IntegerField(default=0)),
                ('days_checkin_possible', models.DateTimeField()),
                ('days_checkout_possible', models.DateTimeField()),
                ('hours_price', models.IntegerField(default=0)),
                ('days_price', models.IntegerField(default=0)),
                ('check_hours', models.BooleanField(default=True)),
                ('sale_hours_price', models.IntegerField(default=0)),
                ('sale_days_price', models.IntegerField(default=0)),
                ('basic_info', models.TextField(default='')),
                ('reservation_notice', models.TextField(default='')),
                ('cancel_regulation', models.TextField(default='')),
                ('reserved', models.ManyToManyField(related_name='reserved', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Stay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=100)),
                ('built_date', models.DateField()),
                ('remodeled_date', models.DateField()),
                ('check_franchise', models.BooleanField(default=False)),
                ('check_new_or_remodeling', models.BooleanField(default=False)),
                ('introduce', models.TextField()),
                ('service_kinds', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(1, '주차가능'), (2, '레스토랑'), (3, '커피숍'), (4, '유료세탁'), (5, '객실금연'), (6, '연회장'), (7, '비즈니스'), (8, '와이파이'), (9, '조식운영'), (10, '스파/월풀'), (11, '수영장'), (12, '파티룸'), (13, '커플PC'), (14, '무인텔'), (15, '바베큐'), (16, '족구장')], max_length=38, null=True)),
                ('service_introduce', models.TextField(default='')),
                ('service_notice', models.TextField()),
                ('pickup_notice', models.TextField(default='')),
                ('directions', models.TextField(default='')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET, related_name='stays', to='stay.Category')),
                ('like', models.ManyToManyField(related_name='like_stay', to=settings.AUTH_USER_MODEL)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stays', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['category'],
            },
        ),
        migrations.AddField(
            model_name='room',
            name='stay',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='stay.Stay'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reservations', to='stay.Room'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='stay',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reservations', to='stay.Stay'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='image',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images_room', to='stay.Room'),
        ),
        migrations.AddField(
            model_name='image',
            name='stay',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images_stay', to='stay.Stay'),
        ),
        migrations.AddField(
            model_name='comment',
            name='stay',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='stay.Stay'),
        ),
        migrations.AddField(
            model_name='comment',
            name='username',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to=settings.AUTH_USER_MODEL),
        ),
    ]