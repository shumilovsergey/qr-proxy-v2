from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Users
from .models import Routers
from .models import Chats
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from project.const import DOMAIN_NAME
from .tg_def import message_get
from .tg_def import message_send
from .tg_def import message_edit
from .tg_def import message_delete
from .tg_def import qr_create
from .tg_def import photo_send
from .serializers import ChatSerializer
import json
import requests

MENU_BUTTON = {
        "inline_keyboard" :  [
            [
                {'text': 'Меню', 'callback_data': 'menu'}
            ]
        ]
    }


def home(request):
    return render(request, 'app/page_1.html')

class UserView(APIView):
    def post(self, request):
        status = True
        code = "200"
        description = "none"

        #REQUEST CHECK
        try:
            user_name = request.data["user_name"]
            user_pass = request.data["user_pass"]
            user_mail = request.data["user_mail"]
        except:
            status = False
            code = "400"
            description = "bad request. correct form { user_name, user_pass, user_mail }"

        #USER_NAME CHECK
        if status:
            try:
                user = Users.objects.get(user_name=user_name)
                code = "400"
                description = " user_name already exist"
                status = False
            except:
                pass

        #EMAIL CHECK
        if status:
            try:
                user = Users.objects.get(user_mail=user_mail)
                code = "400"
                description = "user_mail already exist"
                status = False
            except:
                pass
        
        #ADD USER
        if status:
            Users.objects.create(
                user_name=user_name,
                user_pass=user_pass,
                user_mail=user_mail
            )

        #RESPONSE
        response = {
            "status" : {
                "code" : code,
                "description": description
            },
            "data" : {
                "user_name" : user_name,
                "user_mail" : user_mail,
            }
        }

        return Response(response)
  
class SigninView(APIView):
    def post(self, request):
        status = True
        user_name = "none"
        user_mail = "none"
        code = "200"
        description = "none"

        # REQUEST CHECK
        try:
            user_mail = request.data["user_mail"]
            user_pass = request.data["user_pass"]
        except:
            status = False
            code = "400"
            description = "bad request. correct form { user_mail, user_pass }"       
        # USER_NAME CHAECK
        if status:
            try:
                user = Users.objects.get(user_mail=user_mail)
            except:
                status = False
                code = "400"
                description = "no user with this user_mail"
        # USER_PASS CHECK
        if status:
            if user.user_pass != user_pass:
                status = False
                code = "400"
                description = "wrong password"
            else:
                code = "200"
                description = "none"
                user_name = user.user_name
                user_mail = user.user_mail
        # SESSION
        if status:
            login(request, user)
            request.session['user_id'] = user.id
            print(user.id)
        # RESPONSE
        response = {
            "status" : {
                "code" : code,
                "description": description
            },
            "data" : {
                "user_name" : user_name,
                "user_mail" : user_mail,
            }
        }        
        
        return Response(response)

class LogoutView(APIView):
    def post(self, request):
        user_mail = "none"
        user_name = "none"
        code = "200"
        description = "none"
        status=True

        try:
            user_id = request.session['user_id']
        except:
            status=False
            code = "400"
            description = "user not signin"

        if status:
            request.session['user_id'] = "none"
            description = "logout done"

        response = {
            "status" : {
                "code" : code,
                "description": description
            }
        }
        return Response(response)

class RoutersView(APIView):
    def get(self, request):
        routers_json=[]
        id = 0
        user_mail = "none"
        user_name = "none"
        code = "200"
        description = "none"
        routers_json = "none"
        status=True
        # SIGNIN CHECK
        try:
            user_id = request.session['user_id']
            user = Users.objects.get(id=user_id)
            user_mail = user.user_mail
            user_name = user.user_name     
        except:
            status=False
            code = "400"
            description = "user not signin"
        # ROUTERS RESPONSE
        if status:
            routers = Routers.objects.filter(user_id=user_id)
            if len(routers) == 0:
                description = "user dont have routers"
                routers_json = "none"
            else:
                for rout in routers:
                    public_url = rout.public_url
                    privat_url = rout.privat_url
                    rout_id = rout.id
                    string = {
                        id :{
                            "public_url" : public_url,
                            "privat_url" : privat_url,
                            "rout_id" : rout_id
                        }
                    }
                    id += 1
                    routers_json.append(string)

        # RESPONSE
        response = {
            "status" : {
                "code" : code,
                "description": description
            },
            "data" : {
                "routers" : routers_json
            }
        }        
        return Response(response)

    def post(self, request):
        routers_json=[]
        id = 0
        user_mail = "none"
        user_name = "none"
        code = "200"
        description = "none"
        status=True
        # DATA CHECK
        try:
            privat_url = request.data["privat_url"]
        except:
            status=False
            code="400"
            description="bad request. correct form [ privat_url ]"
        # SIGNIN CHECK
        if status:
            try:
                user_id = request.session['user_id']
                user = Users.objects.get(id=user_id)
                user_mail = user.user_mail
                user_name = user.user_name     
            except:
                status=False
                code = "400"
                description = "user not signin"
        
        if status:
            Routers.objects.create(user_id=user_id, privat_url=privat_url)
            routers = Routers.objects.filter(user_id=user_id)

            for rout in routers:
                if rout.privat_url == privat_url and rout.public_url == "none":
                    rout_id = rout.id
                    public_url = f"{DOMAIN_NAME}/api/redirect/{rout_id}/"
                    rout = Routers.objects.get(id=rout_id)
                    rout.public_url = public_url
                    rout.save()
                else:
                    code = "400"
                    description = "rout.id problems. zvonite serege"

            # ROUTERS ARRAY
            if status:
                routers = Routers.objects.filter(user_id=user_id)
                if len(routers) == 0:
                    description = "user dont have routers"
                    routers_json = "none"
                else:

                    for rout in routers:
                        public_url = rout.public_url
                        privat_url = rout.privat_url
                        rout_id = rout.id
                        string = {
                            id :{
                                "public_url" : public_url,
                                "privat_url" : privat_url,
                                "rout_id" : rout_id
                            }
                        }
                        id += 1
                        routers_json.append(string)
        response = {
            "status" : {
                "code" : code,
                "description": description
            },
            "data" : {
                "routers" : routers_json
            }
        }                    
        return Response(response)
        
    def delete(self, request):
        user_mail = "none"
        user_name = "none"
        code = "200"
        description = "none"
        status=True
        # DATA CHECK
        try:
            rout_id = request.data["rout_id"]
        except:
            status=False
            code="400"
            description="bad request. correct form [ rout_id ]"
        # SIGNIN CHECK
        if status:
            try:
                user_id = request.session['user_id']
                user = Users.objects.get(id=user_id)
                user_mail = user.user_mail
                user_name = user.user_name     
            except:
                status=False
                code = "400"
                description = "user not signin"
        #
        if status:
            try:
                rout = Routers.objects.get(id=rout_id)
                rout.delete()
            except:
                status=False
                code = "400"
                description = "bad request. no such rout"    
                            
        response = {
            "status" : {
                "code" : code,
                "description": description
            }
        }      
        return Response(response)

    def put(self, request):
        user_mail = "none"
        user_name = "none"
        code = "200"
        description = "none"
        status=True
        # DATA CHECK
        try:
            rout_id = request.data["rout_id"]
            privat_url = request.data["privat_url"]

        except:
            status=False
            code="400"
            description="bad request. correct form [ rout_id, privat_url]"
        # SIGNIN CHECK
        if status:
            try:
                user_id = request.session['user_id']
                user = Users.objects.get(id=user_id)
                user_mail = user.user_mail
                user_name = user.user_name     
            except:
                status=False
                code = "400"
                description = "user not signin"
        #
        if status:
            try:
                rout = Routers.objects.get(id=rout_id)
                rout.privat_url = privat_url
                rout.save()
            except:
                status=False
                code = "400"
                description = "bad request. no such rout"    
                            
        response = {
            "status" : {
                "code" : code,
                "description": description
            }
        }      
        return Response(response)

class RedirectView(APIView):
    def get(self, request, rout_id):
        try:
            rout = Routers.objects.get(id=rout_id)
            response=redirect(rout.privat_url)
        except:
            code = "400"
            description = "bad request. no such rout_id"
            response = {
                "code" : code,
                "description": description
            }
        return response

class WebhookView(APIView):
    def post(self, request):
        message = message_get(request)
        print(message)
        chat_id = message["data"]["chat_id"]
        message_id = message["data"]["message_id"]
        text = message["content"]["text"]
        callback = message["data"]["callback"]
        keyboard = "none"

        if text == "/start":
            start(message)

        elif callback == "rout_create":
            text = "Отправьте мне ссылку на ваш сайт"
            message_edit(chat_id, message_id, text, keyboard)
        
        elif callback == "menu":
            message_delete(chat_id, message_id)
            start(message)

        elif callback == "rout_get":
            message_delete(chat_id, message_id)
            user = Chats.objects.get(chat_id=chat_id)
            photo_id = user.qr_id
            text = "Вот ваш QrCode"
            keyboard = MENU_BUTTON
            photo_send(chat_id, text, keyboard, photo_id)
        
        elif callback == "contact":
            message_delete(chat_id, message_id)
            text = "Отзывы и предложения можно отправить по адресу wumilovsergey@gmail.com, либо в телеграме @sergey_showmelove!"
            keyboard = MENU_BUTTON
            message_send(chat_id, text, keyboard)
###___CALLBACK___###
        else:
            user = Chats.objects.get(chat_id=chat_id)

            if user.last_callback == "rout_create":
                rout_create(message, user)

############
            elif user.last_callback == "none":
                message_delete(chat_id, message_id)

        return HttpResponse()

def start(message):
    chat_id = message["data"]["chat_id"]
    chat = {'chat_id' : chat_id }
    serializer = ChatSerializer(data=chat)
    if serializer.is_valid():
        serializer.save()

    user = Chats.objects.get(chat_id=chat_id)
    user.last_callback = "none"
    user.public_url = f"{DOMAIN_NAME}/api/telegram_bot/{chat_id}"
    user.save()

    if user.privat_url == "none":
        keyboard = {
            "inline_keyboard" : [
                [
                    {'text': 'Создать', 'callback_data': 'rout_create'}
                ],
                [
                    {'text': 'Обратная связь', 'callback_data': 'contact'}
                ]
            ]
        }   
    else:
        keyboard = {
            "inline_keyboard" :  [
                [
                    {'text': 'Редактировать', 'callback_data': 'rout_create'}
                ],        
                [
                    {'text': 'Показать', 'callback_data': 'rout_get'}
                ], 
                [
                    {'text': 'Обратная связь', 'callback_data': 'contact'}
                ]                
            ]
        }

    text = "Меню"

    message_send(chat_id, text, keyboard)
    return 

def rout_create(message, user):
    privat_url = message["content"]["text"]
    chat_id = message["data"]["chat_id"]
    message_id = message["data"]["message_id"]
    keyboard = "none"

    url = message["content"]["text"]
    try:
        response = requests.get(url)
        if response.status_code == 200:
            response = 200
        else:
            response = 400
    except:
        response = 400

    if response != 200:
        message_delete(chat_id, message_id)

        text = "Плохая ссылка, попробуйте еще раз!"
        message_id = user.last_id
        message_edit(chat_id, message_id, text, keyboard)
    else:
        message_delete(chat_id, message_id)
        message_id = user.last_id
        message_delete(chat_id, message_id)
        photo_id = qr_create(chat_id, user)

        user.privat_url = privat_url
        user.last_callback = "none"
        user.last_id = "none"
        user.save()

    return

class RedirectTelegramView(APIView):
    def get(self, request, chat_id):

        user = Chats.objects.get(chat_id=chat_id)
        if user.privat_url == "none":
            response = "none"
        else:
            response=redirect(user.privat_url)
        return response