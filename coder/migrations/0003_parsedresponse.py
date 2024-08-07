# Generated by Django 4.1.5 on 2023-05-11 22:38

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('coder', '0002_coder_running'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParsedResponse',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('coder_id', models.UUIDField()),
                ('response', models.TextField()),
                ('parsed_response', models.JSONField()),
                ('error', models.JSONField(null=True)),
                ('parser', models.TextField(max_length=50)),
            ],
        ),
    ]
