from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.

class Completion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    use_case = models.CharField(max_length=50)
    
    message = models.JSONField(null=True)
    response = models.JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    model = models.CharField(max_length=50, null=False)

    error = models.BooleanField(default=False, null=False)
    error_code = models.CharField(null=True, max_length=100)

    context_length_exceeded = models.BooleanField(default=False)