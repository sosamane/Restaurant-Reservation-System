from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from django.contrib.admin.sites import AdminSite
from django.template.response import TemplateResponse
from django.template.loader import get_template
from django.db.models import Count, Avg
from django.utils.dateformat import format
from django.db.models.functions import TruncHour
from datetime import date, timedelta
from .models import Reservation, Table
from io import BytesIO
from xhtml2pdf import pisa
import base64
import csv

class BlueishAdminSite(AdminSite):
    site_header = "Blueish Restaurant Admin"
    site_title = "Blueish Admin Portal"
    index_title = "Welcome to Blueish Restaurant Management"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("analytics/", self.admin_view(self.analytics_view), name="reservation_analytics"),
            path("analytics/export/", self.admin_view(self.export_csv), name="analytics_export_csv"),
            path("analytics/export/pdf/", self.admin_view(self.export_pdf), name="analytics_export_pdf"),
        ]
        return custom_urls + urls

    def analytics_view(self, request):
        today = date.today()
        last_7_days = today - timedelta(days=6)

        qs = Reservation.objects.filter(date__range=(last_7_days, today))
        total = qs.count()
        avg_party = qs.aggregate(avg=Avg("qty_people"))["avg"] or 0

        reservations_by_day = qs.values("date").annotate(count=Count("id")).order_by("date")
        top_tables = qs.values("TableNumber__TableNumber").annotate(count=Count("id")).order_by("-count")[:5]

        chart_labels = [format(r["date"], "Y-m-d") for r in reservations_by_day]
        chart_data = [r["count"] for r in reservations_by_day]
        table_labels = [f"Table {r['TableNumber__TableNumber']}" for r in top_tables]
        table_data = [r["count"] for r in top_tables]

        peak_hour_qs = qs.annotate(hour=TruncHour("time")).values("hour").annotate(count=Count("id")).order_by("-count")
        peak_hour = peak_hour_qs[0]["hour"].strftime("%I:%M %p") if peak_hour_qs else "N/A"

        context = self.each_context(request)
        context.update({
            "total_reservations": total,
            "average_party_size": avg_party,
            "chart_labels": chart_labels,
            "chart_data": chart_data,
            "table_labels": table_labels,
            "table_data": table_data,
            "peak_hour": peak_hour,
            "reservations_by_day": reservations_by_day,
            "top_tables": top_tables,
        })
        return TemplateResponse(request, "admin/analytics.html", context)

    def export_csv(self, request):
        qs = Reservation.objects.all().order_by("-date", "-time")
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="reservation_analytics.csv"'

        writer = csv.writer(response)
        writer.writerow(["Name", "Email", "Phone", "Date", "Time", "Table", "Guests"])
        for r in qs:
            writer.writerow([
                r.name, r.email, r.phonenumber, r.date, r.time,
                r.TableNumber.TableNumber, r.qty_people
            ])
        return response

    def export_pdf(self, request):
        response = self.analytics_view(request)
        context = response.context_data
        with open("reservations/static/admin/img/BlueishRestaurantLogo.jpg", "rb") as image_file:
            context["base64_logo"] = base64.b64encode(image_file.read()).decode("utf-8")

        template = get_template("admin/analytics_pdf.html")
        html = template.render(context)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), dest=result)
        if pdf.err:
            return HttpResponse("PDF generation failed", status=500)

        return HttpResponse(result.getvalue(), content_type="application/pdf")

blueish_admin_site = BlueishAdminSite(name="blueish_admin")

@admin.register(Table, site=blueish_admin_site)
class TableAdmin(admin.ModelAdmin):
    list_display = ("TableNumber", "SeatCapacity")
    search_fields = ("TableNumber",)
    ordering = ("TableNumber",)

@admin.register(Reservation, site=blueish_admin_site)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "date", "time", "qty_people", "TableNumber")
    list_filter = ("date", "TableNumber")
    search_fields = ("name", "email", "phonenumber")
    ordering = ("-date", "time")
    fieldsets = (
        ("Customer Info", {
            "fields": ("name", "email", "phonenumber")
        }),
        ("Booking Details", {
            "fields": ("date", "time", "duration_minutes", "qty_people", "TableNumber")
        }),
    )
