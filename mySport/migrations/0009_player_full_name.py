# Generated by Django 3.1.7 on 2021-03-25 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mySport', '0008_playerseasonstats_team_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='full_name',
            field=models.CharField(default='NA', max_length=100),
        ),
    ]
