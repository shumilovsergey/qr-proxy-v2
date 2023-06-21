from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Users
from .models import Routers
from django.contrib.auth import authenticate, login
import json


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
        response = json_response(user_name=user_name, user_mail=user_mail, code=code, description=description)

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
        response = json_response(user_name=user_name, user_mail=user_mail, code=code, description=description)
        
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

        response = json_response(user_name=user_name, user_mail=user_mail, code=code, description=description)
        return Response(response)

class RoutersView(APIView):
    def post(self, request):
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
                routers_json=[]
                id = 0
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

        response = json_response(user_name=user_name, user_mail=user_mail, code=code, description=description, routers=routers_json)
        return Response(response)

    def put(self, request):
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
                    public_url = f"http://domain.name/routers/{user_id}/{rout_id}/"
                    rout = Routers.objects.get(id=rout_id)
                    rout.public_url = public_url
                    rout.save()
                else:
                    code = "400"
                    description = "rout.id problems. zvonite serege"

            response = json_response(user_name=user_name, user_mail=user_mail, code=code, description=description)
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

        response = json_response(user_name=user_name, user_mail=user_mail, code=code, description=description)       
        return Response(response)
        
######    
def json_response(code, description, user_name, user_mail, routers="none"):
        response = {
            "status" : {
                "code" : code,
                "description": description
            },
            "data" : {
                "user_name" : user_name,
                "user_mail" : user_mail,
                "routers"   : routers
            }
        }
        return response