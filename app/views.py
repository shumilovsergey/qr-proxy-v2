from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import UsersSerializer



def home(request):
    return render(request, 'app/page_1.html')

class HelloWorldView(APIView):
    def get(self, request):
        data = {"message": "Hello, leha lepeha"}
        return Response(data)
    

class RegistrationView(APIView):
    def post(self, request):
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = json_resp("0", "0")
        else:
            error_code = serializer.errors["non_field_errors"][0]
            response = json_resp("400", error_code)
        return Response(response)
    
def json_resp(error_code, error_message):
    response = {
        "status" : {
            "error_code": error_code,
            "error_message": error_message
        }
    }
    return response