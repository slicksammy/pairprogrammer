# Generated by Django 4.1.5 on 2023-06-27 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coder', '0010_coder_recipe'),
    ]

    operations = [
        migrations.AddField(
            model_name='codermessage',
            name='system_command',
            field=models.BooleanField(default=False),
        ),
    ]
