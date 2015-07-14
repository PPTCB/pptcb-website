from django.conf import settings


def full_url_name(request):
    name_list = request.resolver_match.namespaces
    name_list.append(request.resolver_match.url_name)
    return {'full_url_name': ':'.join(name_list)}


def installed_apps(request):
    return {'installed_apps': settings.INSTALLED_APPS}