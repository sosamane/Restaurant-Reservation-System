from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.utils.dateparse import parse_date, parse_time
from django.utils.timezone import now
from django.db.models import Q
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib import messages

from datetime import datetime, timedelta

from .models import Table, Reservation
from .forms import ReservationForm
from .utils import generate_reservation_pdf

#-----------------------------------------------------------------------------------------------

# make_reservation view
def make_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()

            # Email content
            subject = 'Your Reservation at Blueish Restaurant'
            from_email = 'blueishrestaurant@gmail.com'
            to_email = reservation.email

            text_content = f"""
            Hello {reservation.name},

            Your reservation for {reservation.date} at {reservation.time} for {reservation.qty_people} people is confirmed.

            Thank you for booking with Blueish Restaurant!
            """

            html_content = render_to_string('reservations/confirmation_email.html', {
                'reservation': reservation
            })

            email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
            email.attach_alternative(html_content, "text/html")

            # 🔥 Attach the PDF
            pdf_file = generate_reservation_pdf(reservation)
            email.attach(f"Reservation_Confirmation_{reservation.name}.pdf", pdf_file.read(), 'application/pdf')

            email.send()
            
            return redirect('reservation_complete')
    else:
        form = ReservationForm()

    return render(request, 'reservations/make_reservation.html', {'form': form})
#-----------------------------------------------------------------------------------------------

# reservation_complete view
def reservation_complete(request):
    return render(request, 'reservations/reservation_booked.html')

#-----------------------------------------------------------------------------------------------

# API view: available tables for a given date and time
@require_GET
def available_tables(request):
    date_str = request.GET.get('date')
    time_str = request.GET.get('time')
    guests_str = request.GET.get('guests')  #Optional guest count

    if not date_str or not time_str:
        return JsonResponse({'error': 'Missing date or time'}, status=400)

    try:
        reservation_date = parse_date(date_str)
        reservation_time = parse_time(time_str)
        guest_count = int(guests_str) if guests_str else 0

        requested_start = datetime.combine(reservation_date, reservation_time)
        requested_end = requested_start + timedelta(minutes=60)  # 1-hour default

        # Find conflicting reservations
        conflicting_reservations = Reservation.objects.filter(
            date=reservation_date
        ).exclude(
            time__gte=(requested_end.time())
        ).exclude(
            time__lte=(requested_start - timedelta(minutes=60)).time()
        )

        booked_table_ids = conflicting_reservations.values_list('TableNumber_id', flat=True)

        # Only show available tables (and optionally filter by seat capacity)
        tables_qs = Table.objects.exclude(id__in=booked_table_ids)
        if guest_count > 0:
            tables_qs = tables_qs.filter(SeatCapacity__gte=guest_count)

        available_data = [{
            'id': t.id,
            'TableNumber': t.TableNumber,
            'SeatCapacity': t.SeatCapacity,
        } for t in tables_qs]

        return JsonResponse({'available_tables': available_data})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

#------------------------------------------------------------------------------------------------
#looks up reservations
def lookup_reservations(request):
    reservations = []
    email_query = ''

    if request.method == 'POST':
        if 'cancel_id' in request.POST:
            # 🔥 Cancel booking
            reservation_id = request.POST.get('cancel_id')
            Reservation.objects.filter(id=reservation_id).delete()
            messages.success(request, "Your booking has been cancelled.") # type: ignore
        else:
            # 🔍 Search by email
            email_query = request.POST.get('email')
            if email_query:
                reservations = Reservation.objects.filter(
                    email__iexact=email_query,
                    date__gte=now().date()
                ).order_by('date', 'time')

    return render(request, 'reservations/lookup.html', {
        'reservations': reservations,
        'email_query': email_query
    })

#------------------------------------------------------------------------------

def home(request):
    return render(request, 'reservations/home.html')
