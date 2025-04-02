from django.db import models
from django.utils import timezone


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"

    class Meta:
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['phone_number']),
        ]


class RestaurantTable(models.Model):
    TABLE_STATUS_CHOICES = [
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('occupied', 'Occupied'),
    ]

    table_number = models.IntegerField(unique=True)
    capacity = models.IntegerField()
    status = models.CharField(
        max_length=10,
        choices=TABLE_STATUS_CHOICES,
        default='available'
    )

    def __str__(self):
        return f"Table {self.table_number} (Capacity: {self.capacity})"


class Booking(models.Model):
    BOOKING_STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    customer = models.ForeignKey(
        Customer, 
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    table = models.ForeignKey(
        RestaurantTable,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    booking_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(
        max_length=10,
        choices=BOOKING_STATUS_CHOICES,
        default='confirmed'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Booking for {self.customer.name} on {self.booking_date} at {self.start_time}"

    class Meta:
        indexes = [
            models.Index(fields=['booking_date']),
            models.Index(fields=['status']),
        ]