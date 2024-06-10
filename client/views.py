import copy
import json

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View

import dashboard_bo.login_control as bo_login
import dashboard_bo.produto as bo_produto
import dashboard_bo.search as bo_search
import dashboard_bo.sellers as bo_sellers

from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
from http import HTTPStatus
from django.views.decorators.csrf import csrf_exempt


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


class WebScrapView(View):
    """
    Essa class é responsavel pelo render do webScrap Page
    """
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """
        Requisição get
        :param request: dados da requisição
        :param args: parametros extras
        :param kwargs: parametros extras
        :return: Render page
        """
        return render(request=request, template_name='content-webscrap.html')


class ProdutoView(View):
    """
    Essa class é responsavel pelo render do Produtos page
    """
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """
        Requisição get
        :param request: dados da requisição
        :param args: parametros extras
        :param kwargs: parametros extras
        :return: Render page
        """
        return render(request=request, template_name='content-produto.html')


class AjaxProdutosView(View):
    """
    Essa class é responsavel pelo json do Produtos page
    """
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """
        Requisição get
        :param request: dados da requisição
        :param args: parametros extras
        :param kwargs: parametros extras
        :return: Render page
        """
        context = bo_produto.Produto.get_all_products_filtered()
        return JsonResponse(context, safe=False)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        content = copy.deepcopy(request.POST)
        del content['csrfmiddlewaretoken']
        bo_produto.Produto().set_product(content)
        return JsonResponse('', safe=False)


class AjaxProductHistoric(View):

    def get(self, request, *args, **kwargs):
        ean = kwargs['ean']
        context = bo_produto.Produto(ean=ean).get_all_product_historic()
        return JsonResponse(context, safe=False)


class AjaxProductEditHistoric(View):

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        bo_produto.Produto.edit_product_historic(body['data'])
        return JsonResponse('', safe=False)

    @csrf_exempt
    def delete(self, request, *args, **kwargs):
        body = json.loads(request.body)
        bo_produto.Produto.delete_product_historic(body['data'])
        return JsonResponse('', safe=False)


class AjaxPesquisaView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        request_filter = request.GET.get('search')
        context = bo_search.SearchProduct.search_ean_product(request_filter)
        return JsonResponse(context, safe=False)


class AjaxGetProdutoGraph(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        ean = request.GET.get('ean')
        context = bo_produto.Produto(ean=ean).get_product_2_graph()
        return JsonResponse(context, safe=False)


class AjaxGetAllSellers(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = bo_sellers.Seller.get_all_sellers()
        return JsonResponse(context, safe=False)
