from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
import dashboard_bo.login_control as bo_login
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
from http import HTTPStatus


class LoginView(View):
    """
    Essa clase é responsavel pelo login/auth do usuario
    """
    def get(self, request, *args, **kwargs):
        """
        Requisição get
        :param request: dados da requisição
        :param args: parametros extras
        :param kwargs: parametros extras
        :return: Render da pagina login HTML
        """
        return render(request=request, template_name='login.html')

    def post(self, request, *args, **kwargs):
        """
        Requisição post
        :param request: dados da requisição
        :param args: parametros extras
        :param kwargs: parametros extras
        :return: Json response com status do login
        """
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            bo_login.LoginControl(username=username, password=password).authenticate_user(request=request)
            return JsonResponse('', safe=False)
        except ValidationError:
            return JsonResponse(data='', safe=False, status=HTTPStatus.FORBIDDEN)


class LogoffView(View):
    """
    Essa class é responsavel pelo Logoff do usuario
    """
    def get(self, request, *args, **kwargs):
        """
        Requisição get
        :param request: dados da requisição
        :param args: parametros extras
        :param kwargs: parametros extras
        :return: Redirect para pagina de login
        """
        bo_login.LoginControl.logoff_user(request=request)
        return redirect(settings.LOGIN_URL)


class DashboardView(View):
    """
    Essa classe é responsavel pela pagina principal do sistema
    """
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """
        Requisição get
        :param request: dados da requisição
        :param args: parametros extras
        :param kwargs: parametros extras
        :return: Render da pagina dashboard  HTML
        """
        return render(request=request, template_name='dashboard.html')
