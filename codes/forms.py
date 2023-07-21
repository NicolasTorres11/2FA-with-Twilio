from django import forms
from .models import Codes


class CodeForm(forms.ModelForm):
    number = forms.CharField(label='Code', help_text='Ingrese El Mensaje de Texto Que llego a su telefono')

    class Meta:
        model = Codes
        fields = ('number',)
