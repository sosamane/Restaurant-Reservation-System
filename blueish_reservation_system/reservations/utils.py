from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from django.conf import settings
import os

def generate_reservation_pdf(reservation):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Draw logo (optional)
    logo_path = os.path.join(settings.BASE_DIR, 'reservations', 'static', 'reservations', 'BlueishRestaurantLogo.jpg')
    if os.path.exists(logo_path):
        pdf.drawImage(logo_path, 50, height - 130, width=100, preserveAspectRatio=True, mask='auto')

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, height - 150, "Reservation Confirmation")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, height - 180, f"Name: {reservation.name}")
    pdf.drawString(50, height - 200, f"Email: {reservation.email}")
    pdf.drawString(50, height - 220, f"Phone: {reservation.phonenumber}")
    pdf.drawString(50, height - 240, f"Date: {reservation.date}")
    pdf.drawString(50, height - 260, f"Time: {reservation.time}")
    pdf.drawString(50, height - 280, f"Guests: {reservation.qty_people}")
    pdf.drawString(50, height - 300, f"Table: {reservation.TableNumber}")

    pdf.setFont("Helvetica-Oblique", 10)
    pdf.drawString(50, height - 340, "Thank you for booking with Blueish Restaurant 🦞")

    pdf.showPage()
    pdf.save()
    buffer.seek(0)

    return buffer
