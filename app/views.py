from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Users
from django.contrib.auth import authenticate, login



def home(request):
    return render(request, 'app/page_1.html')

class UserView(APIView):
    def post(self, request):
        status = True

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
            code = "200"
            description = "none"

        #RESPONSE
        response = {
            "status" : {
                "code": code,
                "description": description
            }
        }
        return Response(response)
  
class SigninView(APIView):
    def post(self, request):
        status = True
        user_name = "none"
        user_mail = "none"
        # REQUEST CHECK
        try:
            user_name = request.data["user_name"]
            user_pass = request.data["user_pass"]
        except:
            status = False
            code = "400"
            description = "bad request. correct form { user_name, user_pass }"       
        # USER_NAME CHAECK
        if status:
            try:
                user = Users.objects.get(user_name=user_name)
            except:
                status = False
                code = "400"
                description = "no user with this user_name"
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
            request.session['is_authorized'] = True

        # RESPONSE
        response = {
            "status" : {
                "code" : code,
                "description": description
            },
            "data" : {
                "user_name" : user_name,
                "user_mail" : user_mail
            }
        }
        return Response(response)

                