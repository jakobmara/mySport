# Generated by Django 3.1.7 on 2021-03-25 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mySport', '0013_auto_20210325_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teamseasonstats',
            name='defensive_rating',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='teamseasonstats',
            name='offensive_rating',
            field=models.FloatField(default=0.0),
        ),
    ]