from .models import Message
from django.contrib.contenttypes.models import ContentType

class Interface:
    def __init__(self, model, object_id):
        self.model = model
        self.object_id = object_id

    def list(self):
        return list(Message.objects.filter(message_type=ContentType.objects.get_for_model(self.model), object_id=self.object_id).order_by('created_at'))

    def create_message(self, message_content):
        return Message.objects.create(
            message_type=ContentType.objects.get_for_model(self.model),
            message_content=message_content,
            object_id=self.object_id
        )