# Generated by Django 3.1.7 on 2021-03-21 22:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mySport', '0005_auto_20210321_1803'),
    ]

    operations = [
        migrations.RenameField(
            model_name='playerseasonstats',
            old_name='three_points_percentage',
            new_name='three_point_percentage',
        ),
    ]
