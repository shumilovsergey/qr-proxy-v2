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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)