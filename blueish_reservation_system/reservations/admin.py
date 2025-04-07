from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.staticfiles.storage import staticfiles_storage
from .models import Reservation, Table

class BlueishAdminSite(AdminSite):
    site_header = "Blueish Restaurant Admin"
    site_title = "Blueish Admin Portal"
    index_title = "Welcome to Blueish Restaurant Management"

    def each_context(self, request):
        context = super().each_context(request)
        context['custom_css'] = staticfiles_storage.url('admin/css/custom.css')
        return context

blueish_admin_site = BlueishAdminSite(name='blueish_admin')


@admin.register(Table, site=blueish_admin_site)
class TableAdmin(admin.ModelAdmin):
    list_display = ('TableNumber', 'SeatCapacity')
    search_fields = ('TableNumber',)
    ordering = ('TableNumber',)

@admin.register(Reservation, site=blueish_admin_site)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'date', 'time', 'qty_people', 'TableNumber')
    list_filter = ('date', 'TableNumber')
    search_fields = ('name', 'email', 'phonenumber')
    ordering = ('-date', 'time')

    fieldsets = (
        ("Customer Info", {
            'fields': ('name', 'email', 'phonenumber')
        }),
        ("Booking Details", {
            'fields': ('date', 'time', 'duration_minutes', 'qty_people', 'TableNumber')
        }),
    )
