# Generated by Django 4.2.5 on 2023-10-06 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Admin_User',
        ),
        migrations.AddField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=True),
        ),
    ]
