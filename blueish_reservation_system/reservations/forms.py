from django import forms
from .models import Reservation
import re
import datetime

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = [
            'name',
            'phonenumber',
            'email',
            'date',
            'time',
            'qty_people',
            'TableNumber',
        ]

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your full name'}),
            'phonenumber': forms.TextInput(attrs={'placeholder': '11-digit UK number'}),
            'email': forms.EmailInput(attrs={'placeholder': 'your@email.com'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'qty_people': forms.NumberInput(attrs={'min': 1, 'placeholder': 'e.g. 4'}),
            'TableNumber': forms.Select()
        }

        labels = {
            'qty_people': 'Number of People',
            'TableNumber': 'Available Tables'
        }

    def clean_phonenumber(self):
        number = self.cleaned_data['phonenumber']
        if not re.match(r'^\d{11}$', number):
            raise forms.ValidationError("Phone number must be 11 digits.")
        return number

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < datetime.today().date():
            raise forms.ValidationError("You can't book for a past date.")
        return date
