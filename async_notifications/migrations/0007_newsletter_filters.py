# Generated by Django 3.1.1 on 2020-09-22 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('async_notifications', '0006_newslettertask_task_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsletter',
            name='filters',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Form filters'),
        ),
    ]