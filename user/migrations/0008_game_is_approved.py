# Generated by Django 4.2.5 on 2023-10-27 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_location_hint_game_location_game_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
