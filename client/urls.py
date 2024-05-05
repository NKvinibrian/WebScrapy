from django.urls import path
from client.views import *

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logoff', LogoffView.as_view(), name='logoff'),

    path('web-scrap', WebScrapView.as_view(), name='web_scrap'),

    path('produtos', ProdutoView.as_view(), name='produtos'),
    path('ajax-produtos', AjaxProdutosView.as_view(), name='ajax_produtos'),

    path('pesquisa', AjaxPesquisaView.as_view(), name='ajax_pesquisa'),
    path('produto-graph', AjaxGetProdutoGraph.as_view(), name='ajax_produto_graph'),

    path('', DashboardView.as_view(), name='dashboard')
]
