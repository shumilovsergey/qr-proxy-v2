from django.urls import path
from . import views 
from .views import RegistrationView
from .views import HelloWorldView

urlpatterns = [
    path('', views.home, name='home'),
    path('api/hello/', HelloWorldView.as_view(), name='hello-world'),
    path('api/register/', RegistrationView.as_view(), name='user-registration'),
]