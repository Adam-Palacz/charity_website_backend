# Generated by Django 3.2.4 on 2021-06-16 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charity_app', '0005_auto_20210616_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='pick_up_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='donation',
            name='pick_up_time',
            field=models.TimeField(null=True),
        ),
    ]