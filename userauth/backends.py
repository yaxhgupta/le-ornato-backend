from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailOrContactBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Allow login with either email OR contact_no.
        """
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(contact_no=username)
            except User.DoesNotExist:
                return None

        if user.check_password(password):
            return user
        return None
