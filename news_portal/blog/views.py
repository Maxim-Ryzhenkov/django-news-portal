from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Привет. Вы на главной страничке блога.")
