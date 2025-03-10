from django.shortcuts import render, redirect
from .forms import ReservationForm

def reserve_table(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  # Redirect to a success page
    else:
        form = ReservationForm()
    return render(request, 'reservations/reservation_form.html', {'form': form})

def success(request):
    return render(request, 'reservations/success.html')
