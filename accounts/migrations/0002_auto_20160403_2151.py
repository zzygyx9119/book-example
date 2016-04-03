# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('uid', models.CharField(default=uuid.uuid4, max_length=36)),
            ],
        ),
        migrations.AlterField(
            model_name='listuser',
            name='email',
            field=models.EmailField(serialize=False, primary_key=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='listuser',
            name='groups',
            field=models.ManyToManyField(help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups', related_name='user_set', blank=True, related_query_name='user', to='auth.Group'),
        ),
        migrations.AlterField(
            model_name='listuser',
            name='last_login',
            field=models.DateTimeField(null=True, verbose_name='last login', blank=True),
        ),
        migrations.AlterField(
            model_name='listuser',
            name='user_permissions',
            field=models.ManyToManyField(help_text='Specific permissions for this user.', verbose_name='user permissions', related_name='user_set', blank=True, related_query_name='user', to='auth.Permission'),
        ),
    ]
