from django import forms
from . import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.forms import DateTimeInput

class ServiceOrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        if 'service_time' not in initial:
            initial['service_time'] = timezone.now().replace(second=0, microsecond=0)
        kwargs['initial'] = initial

        super().__init__(*args, **kwargs)

        barber_choices = [(barber.id, barber.get_full_name()) for barber in models.User.objects.filter(is_staff=True)]
        self.fields['barber'].choices = barber_choices
        self.fields['barber'].label = 'Choose a barber:'
        service_choices = [(service.id, service.name) for service in models.Service.objects.all()]
        self.fields['service'].choices = service_choices
        self.fields['service'].label = 'Choose a service:'

    class Meta:
        model = models.ServiceOrder
        fields = ['barber', 'service', 'service_time']
        labels = {
            'service_time': 'Choose a service time:',
        }
        widgets = {
            'service_time': DateTimeInput(attrs={'type': 'datetime-local'})
        }

    def clean_service_time(self):
        service_time = self.cleaned_data['service_time']
        barber = self.cleaned_data['barber']
        service = self.cleaned_data['service']
        working_hours_start = service_time.replace(hour=10, minute=0, second=0, microsecond=0)
        working_hours_end = service_time.replace(hour=17, minute=0, second=0, microsecond=0)
        if service_time < timezone.now():
            raise ValidationError("Service time cannot be in the past.", code='errorbox')
        if service_time < working_hours_start or service_time + service.duration > working_hours_end:
            raise ValidationError("Service time is outside working hours.", code='errorbox')
        service_end_time = service_time + service.duration
        potentially_overlapping_order = models.ServiceOrder.objects.filter(
            barber=barber,
            service_time__gte=service_time,
        ).order_by("service_time").first()
        if potentially_overlapping_order and potentially_overlapping_order.service_time < service_end_time:
            raise ValidationError("Barber is already booked at this time.", code='errorbox')
        potentially_overlapping_order = models.ServiceOrder.objects.filter(
            barber=barber,
            service_time__lte=service_time,
        ).order_by("service_time").last()
        if potentially_overlapping_order and potentially_overlapping_order.service_time + potentially_overlapping_order.service.duration > service_time:
            raise ValidationError("Barber is already booked at this time.", code='errorbox')
        return service_time
    
class BarberReviewForm(forms.ModelForm):
    class Meta:
        model = models.BarberReview
        fields = ('reviewer', 'content')
        widgets = {
            'reviewer': forms.HiddenInput(),
        }
        labels = {
            'content': '',
        }