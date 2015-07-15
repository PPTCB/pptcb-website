from django.forms import ModelForm

from .models import Composer


class ComposerForm(ModelForm):
    class Meta:
        model = Composer
        fields = ['first_name', 'middle_name', 'last_name']