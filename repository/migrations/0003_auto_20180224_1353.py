# Generated by Django 2.0.1 on 2018-02-24 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0002_auto_20180210_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='ctime',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
