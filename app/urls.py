from django.urls import path
from . import views 
from .views import UserView
from .views import SigninView
from .views import LogoutView
from .views import RoutersView
from .views import RedirectView
from .views import WebhookView
from .views import RedirectTelegramView

urlpatterns = [
    path('', views.home, name='home'),
    path('api/user/', UserView.as_view(), name='user'),
    path('api/auth/signin/', SigninView.as_view(), name='signin'),
    path('api/auth/logout/', LogoutView.as_view(), name='logout'),
    path('api/routers/', RoutersView.as_view(), name='routers'),
    path('api/redirect/<int:rout_id>/', RedirectView.as_view(), name='redirect'),
    path('api/telegram_bot/webhook/', WebhookView.as_view(), name='webhook'),
    path('api/telegram_bot/<int:chat_id>/', RedirectTelegramView.as_view(), name='redirect telegram'),
]