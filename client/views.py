from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
import dashboard_bo.login_control as bo_login
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.


class LoginView(View):

    def get(self, request, *args, **kwargs):
        return render(request=request, template_name='login.html')

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            bo_login.LoginControl(username=username, password=password).authenticate_user(request=request)
            return JsonResponse('', safe=False)
        except ValidationError as e:
            return JsonResponse(e, safe=False)


class LogoffView(LoginView):

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        return response


class DashboardView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request=request, template_name='dashboard.html')
