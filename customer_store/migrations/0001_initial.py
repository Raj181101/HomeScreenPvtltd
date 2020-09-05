# Generated by Django 2.2.16 on 2020-09-04 12:39

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=400)),
                ('slug', models.SlugField(blank=True, max_length=500, null=True, unique=True)),
                ('url', models.URLField(blank=True, max_length=600, null=True)),
                ('source_name', models.CharField(max_length=250)),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('modified_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=48, null=True)),
                ('password', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('mobile', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message='Invalid Number', regex='^(\\+\\d{1,3}[- ]?)?\\d{10}$')])),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profile_pics')),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('modified_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=True)),
                ('langitude', models.CharField(blank=True, max_length=100, null=True)),
                ('latitude', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerBookmark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_bookmarks', models.PositiveIntegerField()),
                ('bookmarks', models.ManyToManyField(blank=True, to='customer_store.Bookmark')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='customer_store.Customer')),
            ],
        ),
    ]