from django import forms
from .models import Reading, Genre

class ReadingForm(forms.ModelForm):
    class Meta:
        model = Reading
        fields = ['date', 'status']
        widgets = {
            'date': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'placeholder': 'Select a date',
                    'type': 'date'
                }
            ),
        }

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']
