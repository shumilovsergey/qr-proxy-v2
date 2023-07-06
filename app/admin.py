from django.contrib import admin
from .models import Users
from .models import Routers
from .models import Chats

admin.site.register(Users)
admin.site.register(Routers)
admin.site.register(Chats)