from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from django.http import HttpResponse

#   IMPORT MODELS!
# from .models import Users

#   EXAMPLE
# def example(request):
#     context = ''
#     return render(request, 'proxy/login.html', {'context':context})

def home(request):
    return render(request, 'app/page_1.html')

class HelloWorldView(APIView):
    def get(self, request):
        data = {"message": "Hello, world!"}
        return Response(data)