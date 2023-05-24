from .models import UserToken
class Interface:
    @classmethod
    def valid_user_api_key(cls, key):
        try:
            UserToken.objects.get(token=key)
            return True
        except UserToken.DoesNotExist:
            return False