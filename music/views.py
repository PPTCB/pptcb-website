from django.http import HttpResponse
from django.shortcuts import render

from .models import MusicalWork, MusicalWorkCategory


def concerts(request):
    return HttpResponse('concerts')


def library(request):
    context = dict()

    # Get active musical works, ordered by their library IDs
    context['musical_works'] = MusicalWork.objects.select_related('category')\
        .prefetch_related('composers', 'arrangers').order_by('library_id')

    # Get next library ID
    if context['musical_works'].count() > 0:
        context['musical_works_next_library_id'] = context['musical_works'].reverse()[0].library_id + 1
    else:
        context['musical_works_next_library_id'] = 1

    # Get grade level choices
    context['musical_work_grade_choices'] = [{'display': choice[1], 'value': choice[0]}
                                             for choice in MusicalWork.GRADE_CHOICES]

    # Get pre-existing categories
    context['musical_work_categories'] = [{'display': category.name, 'value': category.pk} for category in
                                          MusicalWorkCategory.objects.filter(is_active=True).order_by('name')]

    # Render template
    return render(request, 'members/music/library.html', context)


def instruments(request):
    return HttpResponse('instruments')