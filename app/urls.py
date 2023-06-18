from django.urls import path
from . import views 
from .views import UserView
from .views import SigninView

urlpatterns = [
    path('', views.home, name='home'),
    path('api/user/', UserView.as_view(), name='user'),
    path('api/user/auth/signin/', SigninView.as_view(), name='signin'),

]