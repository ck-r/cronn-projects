from django.shortcuts import render, get_object_or_404, redirect
from django.forms import ModelForm, modelform_factory
from appointments.models import Appointment, Patient

AppointmentForm = modelform_factory(Appointment, exclude=[])

# Create your views here.
def index(request):
    return render(request, 'index.html', {
        'alen': len(Appointment.objects.all()),
        'appointments': Appointment.objects.all()
    })

def patient_list(request):
    appointments = Appointment.objects.all()
    patients = []

    for a in appointments:
        if a.patient not in patients:
            patients.append(a.patient)

    return render(request, 'patient_list.html', {
        'patients': patients
    })

def patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    return render(request, 'patient.html', {
        'patient': patient
    })

def appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    return render(request, 'appointment.html', {
        'appointment': appointment
    })

def new_appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")

    else:
        form = AppointmentForm()
        return render(request, "new_appointment.html", context={
            "form": form
        })