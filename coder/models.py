from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Coder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=False, default=User.objects.first().id)
    tasks = models.JSONField(null=False)
    current_task_index = models.IntegerField(null=False)
    files_changed = models.JSONField(null=False, default=dict)
    # max length set to random number
    requirements = models.CharField(null=False, max_length=2000)
    context = models.CharField(null=False, max_length=2000)

    complete = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    running_at = models.DateTimeField(null=True)
    reached_max_length = models.BooleanField(null=False, default=False)

class ParsedResponse(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    coder_id = models.UUIDField(null=False)
    response = models.TextField(null=False)
    # TODO make this nullable and update parse interface to save null on error
    parsed_response = models.JSONField()
    error = models.JSONField(null=True)
    parser = models.TextField(max_length=50, null=False)
