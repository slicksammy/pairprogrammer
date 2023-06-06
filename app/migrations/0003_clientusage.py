# Generated by Django 4.1.5 on 2023-06-06 11:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0002_rename_usertoken_userapikey_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientUsage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_version', models.CharField(max_length=20)),
                ('command', models.CharField(max_length=255)),
                ('exception_class', models.CharField(blank=True, max_length=100, null=True)),
                ('exception_message', models.TextField(blank=True, null=True)),
                ('exception_backtrace', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
