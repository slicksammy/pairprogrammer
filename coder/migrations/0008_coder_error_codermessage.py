# Generated by Django 4.1.5 on 2023-06-26 01:09

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('coder', '0007_alter_coder_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='coder',
            name='error',
            field=models.JSONField(null=True),
        ),
        migrations.CreateModel(
            name='CoderMessage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('role', models.CharField(max_length=50)),
                ('function_name', models.CharField(max_length=50, null=True)),
                ('content', models.TextField(null=True)),
                ('function_call', models.CharField(max_length=100, null=True)),
                ('command', models.JSONField(null=True)),
                ('command_error', models.JSONField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('coder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coder.coder')),
            ],
            options={
                'db_table': 'coder_messages',
            },
        ),
    ]
