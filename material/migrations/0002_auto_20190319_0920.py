# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2019-03-19 03:20
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import material.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('material', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material', models.FileField(upload_to=material.models.upload_path)),
                ('material_name', models.CharField(max_length=256)),
                ('material_description', models.TextField(blank=True, null=True)),
                ('material_serial', models.IntegerField(blank=True, validators=[django.core.validators.MinValueValidator(1)])),
                ('is_deleted', models.BooleanField(default=False)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='material_creator', to=settings.AUTH_USER_MODEL)),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='material_topic', to='material.Topic')),
                ('updater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='material_updater', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='material',
            unique_together=set([('topic', 'material_serial'), ('topic', 'material_name')]),
        ),
    ]
