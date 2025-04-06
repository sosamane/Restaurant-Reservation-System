from django.contrib import admin #imports admin utility

from .models import Table, Reservation #imports table and reservation model classes

#Registers these models:
admin.site.register(Table) #registers Table to admin
admin.site.register(Reservation) #registers Table to admin
