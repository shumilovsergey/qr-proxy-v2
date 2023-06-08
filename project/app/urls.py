from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('api/hello/', views.HelloWorldView.as_view(), name='hello-world'),
]