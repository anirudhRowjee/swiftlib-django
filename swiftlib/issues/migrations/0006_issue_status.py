# Generated by Django 2.1 on 2019-10-27 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0005_merge_20190924_2017'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='status',
            field=models.CharField(choices=[('issued', 'ISSUED'), ('rtrned', 'RETURNED')], default='issued', max_length=8),
        ),
    ]
