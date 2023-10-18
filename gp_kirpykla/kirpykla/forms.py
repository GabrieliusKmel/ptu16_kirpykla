from django import forms
from . import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class ServiceOrderForm(forms.ModelForm):
    class Meta:
        model = models.ServiceOrder
        fields = ['barber', 'service', 'customer', 'service_time', 'status']

    def clean_service_time(self):
        service_time = self.cleaned_data['service_time']
        barber = self.cleaned_data['barber']
        service = self.cleaned_data['service']
        working_hours_start = service_time.replace(hour=10, minute=0, second=0, microsecond=0)
        working_hours_end = service_time.replace(hour=17, minute=0, second=0, microsecond=0)
        if service_time < timezone.now():
            raise ValidationError("Service time cannot be in the past.")
        if service_time < working_hours_start or service_time + service.duration > working_hours_end:
            raise ValidationError("Service time is outside working hours.")
        service_end_time = service_time + service.duration
        potentially_overlapping_order = models.ServiceOrder.objects.filter(
            barber=barber,
            service_time__gte=service_time,
        ).order_by("service_time").first()
        print(potentially_overlapping_order)
        if potentially_overlapping_order and potentially_overlapping_order.service_time < service_end_time:
            raise ValidationError("Barber is already booked at this time.")
        potentially_overlapping_order = models.ServiceOrder.objects.filter(
            barber=barber,
            service_time__lte=service_time,
        ).order_by("service_time").last()
        if potentially_overlapping_order and potentially_overlapping_order.service_time + potentially_overlapping_order.service.duration > service_time:
            raise ValidationError("Barber is already booked at this time.")
        print(potentially_overlapping_order)
        return service_time