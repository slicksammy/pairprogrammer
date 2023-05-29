from .models import UserApiKey
class Interface:
    @classmethod
    def user_from_api_key(cls, key):
        key = UserApiKey.objects.filter(key=key).first()
        if key is not None:
            return key.user