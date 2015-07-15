from django.http import HttpResponse
from django.shortcuts import render

from .forms import ComposerForm
from .models import MusicalWork, MusicalWorkCategory, Composer


def concerts(request):
    return HttpResponse('concerts')


def library(request):
    context = dict()

    # Get active tab
    context['active_tab'] = request.POST.get('active_tab', 'view-library')

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
    context['musical_work_categories'] = MusicalWorkCategory.objects.filter(is_active=True).order_by('name')

    # Get pre-existing composers
    context['composers'] = Composer.objects.filter(is_active=True).order_by('last_name', 'first_name', 'middle_name')

    # Forms
    context['composer_form'] = ComposerForm()

    # Render template
    return render(request, 'members/music/library.html', context)


def instruments(request):
    return HttpResponse('instruments')