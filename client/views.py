from django.shortcuts import render
from django.views import View


# Create your views here.


class LoginView(View):

    def get(self, request, *args, **kwargs):
        return render(request=request, template_name='login.html')

    def post(self, request, *args, **kwargs):
        ...