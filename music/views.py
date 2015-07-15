from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import ComposerForm
from .models import MusicalWork, MusicalWorkCategory, Composer


def concerts(request):
    return HttpResponse('concerts')


def library(request):
    context = {'active_tab': 'request_library'}

    if request.method == 'POST':
        if request.POST.get('function') == 'create_composer':
            composer_form = ComposerForm(request.POST)
            if composer_form.is_valid():
                composer_form.save()
                redirect('members:music:library')
            else:
                context['composer_form'] = composer_form
                context['active_tab'] = 'create_composer'

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
    if 'composer_form' not in context:
        context['composer_form'] = ComposerForm()

    # Render template
    return render(request, 'members/music/library.html', context)


def instruments(request):
    return HttpResponse('instruments')