# Generated by Django 3.1.7 on 2021-04-02 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mySport', '0015_player_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='picture',
            field=models.CharField(default='https://i.imgur.com/fFDjSjA.jpg', max_length=150),
        ),
    ]