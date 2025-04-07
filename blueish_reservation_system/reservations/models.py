#imports models
from django.db import models

#2 model classes

#Table class - stores details about a particular table
class Table(models.Model):
    TableNumber = models.IntegerField(unique=True) #table number variable (int)
    SeatCapacity = models.IntegerField() #seat capacity variable (int)

    #table string method
    def __str__(self):
        return f"Table: {self.TableNumber} - Seats: {self.SeatCapacity}"

#----------------------------------------------------------------------------------

#Reservation class - stores booking reservation details from users
class Reservation(models.Model):
    #booking data
    name = models.CharField(max_length=100) #name variable (max digits: 100) (char)
    phonenumber = models.CharField(max_length=11) #phonenumber variable (max digits: 100) (char)
    TableNumber = models.ForeignKey(Table, on_delete=models.CASCADE) #FK with Table model class | if TableNumber value is deleted = deletes table instance
    email = models.EmailField() #booking email field

    date = models.DateField() #booking date (date)
    time = models.TimeField() #booking time (time)

    duration_minutes = models.IntegerField(default=60)  # How long the table is booked

    qty_people = models.IntegerField() #amount of people (int)

    #Reservation string method
    def __str__(self):
        return f"Booking Reservation for {self.name} (Email: {self.email}) on {self.date} at {self.time}"

