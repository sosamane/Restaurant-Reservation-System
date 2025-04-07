from django.urls import path #imports path utility
from . import views #imports views

urlpatterns = [
    path('make-booking/', views.make_reservation, name='make_reservation'), #reservations/make-booking - make reservation
    path('booking-confirmation/', views.reservation_complete, name='reservation_complete'), #reservations/booking-confirmation - booking completed
    path('api/available-tables/', views.available_tables, name='available_tables'), #API link (available_tables)
    path('lookup/', views.lookup_reservations, name='lookup_reservations'), #lookup webpag
    path('', views.home, name='home'), #homepage
]
