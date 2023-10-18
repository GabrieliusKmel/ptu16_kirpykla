from django import forms
from . import models

class ServiceOrderForm(forms.ModelForm):
    class Meta:
        model = models.ServiceOrder
        fields = ['barber', 'service', 'customer', 'service_time', 'status']

    def clean_service_time(self):
        service_time = self.cleaned_data.get('service_time')
        service_duration = self.cleaned_data.get('service').duration
        models.Service(service_time, service_duration)
        return service_time