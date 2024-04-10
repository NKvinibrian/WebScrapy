from django.urls import path, include
from client.views import LoginView

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    # path('register', include('client.urls')),
    # path('dashboard', include('client.urls'))
]
