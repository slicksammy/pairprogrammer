from django.db import models
import uuid

# Create your models here.
class Coder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tasks = models.JSONField(null=False)
    current_task_index = models.IntegerField(null=False)
    files_changed = models.JSONField(null=False, default=dict)
    # max length set to random number
    requirements = models.CharField(null=False, max_length=2000)
    context = models.CharField(null=False, max_length=2000)

    complete = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)