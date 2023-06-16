from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Users




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
            error_code = "400"
            error_message = "bad request. correct form { user_name, user_pass, user_mail }"

        #USER_NAME CHECK
        if status:
            try:
                user = Users.objects.get(user_name=user_name)
                error_code = "400"
                error_message = " user_name already exist"
                status = False
            except:
                pass

        #EMAIL CHECK
        if status:
            try:
                user = Users.objects.get(user_mail=user_mail)
                error_code = "400"
                error_message = "user_mail already exist"
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
            error_code = "0"
            error_message = "none"

        #RESPONSE
        response = {
            "status" : {
                "error_code": error_code,
                "error_message": error_message
            }
        }
        return Response(response)
  
