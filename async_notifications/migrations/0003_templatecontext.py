# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('async_notifications', '0002_auto_20160515_0018'),
    ]

    operations = [
        migrations.CreateModel(
            name='TemplateContext',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('code', models.CharField(verbose_name='Code', max_length=50)),
                ('context_dic', models.TextField(verbose_name='Context dictionary')),
            ],
            options={
                'verbose_name': 'Context of template',
                'verbose_name_plural': 'Context of template',
            },
        ),
    ]
