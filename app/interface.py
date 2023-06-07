from .models import UserApiKey, UserSignupCode
from django.db.models import Q

class Interface:
    @classmethod
    def user_from_api_key(cls, key):
        key = UserApiKey.objects.filter(key=key).first()
        if key is not None:
            return key.user

    @classmethod
    def signup_code_exists(cls, code):
        return UserSignupCode.objects.filter(Q(code__iexact=code)).exists()