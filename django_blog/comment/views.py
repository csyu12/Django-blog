from django.shortcuts import render, HttpResponse


def index_handler(request):
    return HttpResponse(request)
