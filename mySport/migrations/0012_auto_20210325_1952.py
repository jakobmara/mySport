# Generated by Django 3.1.7 on 2021-03-25 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mySport', '0011_auto_20210325_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teamseasonstats',
            name='season',
            field=models.CharField(default='NA', max_length=10),
        ),
    ]
