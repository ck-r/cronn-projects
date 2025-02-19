from django.utils.timezone import now
from django.db import models

# Create your models here.
class Patient(models.Model):
    last_name = models.CharField(max_length=32)
    first_name = models.CharField(max_length=32)
    city = models.CharField(max_length=96)
    address = models.CharField(max_length=144)
    age = models.IntegerField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Appointment(models.Model):
    date = models.DateTimeField(default=now())
    recommendations = models.CharField(max_length=256)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.date.date()}: {self.patient.last_name}'