from django.http import HttpResponse
from django.shortcuts import render


def concerts(request):
    return HttpResponse('concerts')


def library(request):
    return HttpResponse('library')


def instruments(request):
    return HttpResponse('instruments')