from django.conf.urls import url

from .import views

urlpatterns = [
    url(r'^concerts$', views.concerts, name='concerts$'),
    url(r'^library$', views.library, name='library'),
    url(r'^instruments$', views.instruments, name='instruments'),
]