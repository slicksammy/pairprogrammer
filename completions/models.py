from django.db import models
import uuid
from django.contrib.contenttypes.models import ContentType

# Create your models here.

class Completion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.JSONField()
    response = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    model = models.CharField(max_length=50, null=False)

    completer_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=False)
    completer_id = models.UUIDField(null=False)

    error = models.BooleanField(default=False, null=False)
    error_code = models.CharField(null=True, max_length=100)

    context_length_exceeded = models.BooleanField(default=False)