from django.urls import path
from . import views 
from .views import UserView
from .views import SigninView
from .views import LogoutView
from .views import RoutersView


urlpatterns = [
    path('', views.home, name='home'),
    path('api/user/', UserView.as_view(), name='user'),
    path('api/auth/signin/', SigninView.as_view(), name='signin'),
    path('api/auth/logout/', LogoutView.as_view(), name='logout'),
    path('api/routers/', RoutersView.as_view(), name='routers'),
]