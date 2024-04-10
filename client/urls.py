from django.urls import path, include
from client.views import LoginView, DashboardView, LogoffView

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logoff', LogoffView.as_view(), name='logoff'),
    # path('register', include('client.urls')),
    path('', DashboardView.as_view(), name='dashboard')
]
