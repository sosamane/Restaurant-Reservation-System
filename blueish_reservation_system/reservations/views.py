# reservations/views.py
from django.shortcuts import render, redirect

from .models import Table, Reservation #imports table & reservation models 

from .forms import ReservationForm #imports reservation form class

#make_reservation func (make_reservation view)
def make_reservation(request):
    if request.method == 'POST': #if HTTP request is POST (add to webserver)
        form = ReservationForm(request.POST) #posts the ReservationForm
        if form.is_valid(): #checks if form is valid
            form.save() #saves form
            return redirect('reservation_complete') #redirects URL to 'reservation_complete' URL pathname
    else: #if it doesn't add the form to the server
        form = ReservationForm() #sets form var to it's form

    return render(request, 'reservations/make_reservation.html', {'form': form})

#reservation_complete func (reservation_complete view)
def reservation_complete(request):
    return render(request, 'reservations/reservation_booked.html')