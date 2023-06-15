from django.urls import path
from . import views 
from .views import UserView

urlpatterns = [
    path('', views.home, name='home'),
    path('api/user/', UserView.as_view(), name='user'),
]