from django.db import models
import uuid
from django.contrib.contenttypes.models import ContentType

# Create your models here.

class Completion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField(null=False)
    response = models.JSONField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    model = models.CharField(max_length=50, null=False)

    completer_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    completer_id = models.UUIDField(null=False)
