from django import forms
from .models import Reservation

#booking reservation form
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation #selects Reservation model class (models.py)
        fields = '__all__' #uses all it's fields from that model class
