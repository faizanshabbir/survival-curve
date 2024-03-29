# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survival', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='contactForm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=75)),
                ('message', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
