# Generated by Django 4.1.5 on 2023-06-27 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('completions', '0003_remove_completion_completer_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='completion',
            name='message',
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='completion',
            name='response',
            field=models.JSONField(null=True),
        ),
    ]
