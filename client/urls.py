from django.urls import path
from client.views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('favicon', LoginView.as_view(), name='login'),

    path('login', LoginView.as_view(), name='login'),
    path('logoff', LogoffView.as_view(), name='logoff'),

    path('web-scrap', WebScrapView.as_view(), name='web_scrap'),
    path('ajax-web-scrap', AjaxGetAllSellers.as_view(), name='ajax_web_scrap'),

    path('produtos', ProdutoView.as_view(), name='produtos'),
    path('ajax-produtos', AjaxProdutosView.as_view(), name='ajax_produtos'),
    path('ajax-produtos-historico/<int:ean>', AjaxProductHistoric.as_view(), name='ajax_produtos_historic'),
    path('ajax-produtos-edit-historico', csrf_exempt(AjaxProductEditHistoric.as_view()), name='ajax_edit_historic'),

    path('pesquisa', AjaxPesquisaView.as_view(), name='ajax_pesquisa'),
    path('produto-graph', AjaxGetProdutoGraph.as_view(), name='ajax_produto_graph'),

    path('', DashboardView.as_view(), name='dashboard')
]
