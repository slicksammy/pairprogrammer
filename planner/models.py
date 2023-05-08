from django.db import models
import uuid

# Create your models here.
class Planner(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    requirements = models.CharField(null=False, max_length=2000)
    context = models.CharField(null=False, max_length=2000)
    tasks = models.JSONField(null=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)