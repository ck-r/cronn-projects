from django.contrib import admin
from appointments.models import Patient, Appointment

# Register your models here.
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = 'first_name', 'last_name'

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = 'date',
