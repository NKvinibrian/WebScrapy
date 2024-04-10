from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


class LoginControl:

    def __init__(self, username, password, email):
        self.username = username
        self.email = email
        self.__password = password

    def create_user(self):
        user = User.objects.create_user(self.username, self.email, self.__password)
        user.save()

    def authenticate_user(self):
        user = authenticate(self.username, self.__password)
        if user is not None:
            return user
        else:
            return None
