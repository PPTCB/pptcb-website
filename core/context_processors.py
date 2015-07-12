from django.conf import settings


def installed_apps(request):
    return {'installed_apps' : settings.INSTALLED_APPS}