from django.db import models
from django.contrib.auth.models import User
import uuid


# Create your models here.
class Coder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=False)
    tasks = models.JSONField(null=False)
    current_task_index = models.IntegerField(null=False)
    files_changed = models.JSONField(null=False, default=dict)
    # max length set to random number
    requirements = models.CharField(null=False, max_length=2000)
    context = models.CharField(null=False, max_length=2000)
    recipe = models.CharField(null=False, max_length=50)

    complete = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    running_at = models.DateTimeField(null=True)
    reached_max_length = models.BooleanField(null=False, default=False)
    error = models.JSONField(null=True)

class ParsedResponse(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    coder_id = models.UUIDField(null=False)
    response = models.TextField(null=False)
    # TODO make this nullable and update parse interface to save null on error
    parsed_response = models.JSONField()
    error = models.JSONField(null=True)
    parser = models.TextField(max_length=50, null=False)

class CoderMessage(models.Model):
    # name this coder_messages
    class Meta:
        db_table = 'coder_messages'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    coder = models.ForeignKey(Coder, on_delete=models.CASCADE)
    
    role = models.CharField(max_length=50)
    function_name = models.CharField(null=True,max_length=50)
    content = models.TextField(null=True)
    function_call = models.CharField(null=True, max_length=10000)

    command = models.JSONField(null=True)
    command_error = models.JSONField(null=True)
    system_command = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CoderRecipe(models.Model):
    class Meta:
        db_table = 'coder_recipes'
        unique_together = ('user_id', 'recipe')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=False)
    config = models.JSONField(null=False)
    recipe = models.CharField(null=False, max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)