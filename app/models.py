from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserApiKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class ClientUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    client_version = models.CharField(max_length=20, null=False)
    command = models.CharField(max_length=255)
    exception_class = models.CharField(max_length=100, null=True, blank=True)
    exception_message = models.TextField(null=True, blank=True)
    exception_backtrace = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)