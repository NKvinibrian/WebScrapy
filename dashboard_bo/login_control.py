from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError

class LoginControl:

    def __init__(self, username, password, email=None):
        self.username = username
        self.email = email
        self.__password = password

    def create_user(self):
        user = User.objects.create_user(self.username, self.email, self.__password)
        user.save()

    def authenticate_user(self, request):
        user = authenticate(username=self.username, password=self.__password)
        if user:
            login(request=request, user=user)
        else:
            raise ValidationError("Usuario ou senha invalido")

    @staticmethod
    def logoff_user(request):
        logout(request)
