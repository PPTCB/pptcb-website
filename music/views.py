from django.http import HttpResponse
from django.shortcuts import render

from .models import MusicalWork


def concerts(request):
    return HttpResponse('concerts')


def library(request):
    context = dict()

    # Get active musical works, ordered by their library IDs
    context['musical_works'] = MusicalWork.objects.select_related('category')\
        .prefetch_related('composers', 'arrangers').filter(is_active=True).order_by('library_id')

    # Render template
    return render(request, 'members/music/library.html', context)


def instruments(request):
    return HttpResponse('instruments')