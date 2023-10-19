from typing import Any
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from . import models, forms
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.views.generic import View


def index(request):
    return render(request, "kirpykla/index.html")

def about_us(request):
    about_us_content = models.AboutUs.objects.first()
    return render(
        request,
        "kirpykla/about_us.html",
        {"about_us_content": about_us_content}
    )


class ServiceListView(ListView):
    model = models.Service
    template_name = 'kirpykla/service_list.html'
    context_object_name = 'services'


def book_service(request):
    service_id = request.GET.get('service_id', None)
    if service_id:
        service = get_object_or_404(models.Service, id=service_id)
        initial_data = {'service': service}
    else:
        initial_data = {}

    if request.method == 'POST':
        form = forms.ServiceOrderForm(request.POST)
        if form.is_valid():
            form.instance.customer = request.user
            if service_id:
                form.instance.service = service
            form.save()
            messages.success(request, 'Booking successful!')
            return redirect('book_service')
    else:
        form = forms.ServiceOrderForm(initial=initial_data)

    return render(request, 'kirpykla/booking_form.html', {'form': form})

class ServiceOrderListView(ListView):
    model = models.ServiceOrder
    template_name = 'kirpykla/serviceorder_list.html'
    context_object_name = 'serviceorders'

    def get_queryset(self):
        # Get the currently logged-in user
        user = self.request.user

        # Filter ServiceOrder instances by the user
        queryset = models.ServiceOrder.objects.filter(customer=user)

        return queryset
    
class ServiceOrderCancelView(View):
    def get(self, request, order_id):
        try:
            serviceorder = models.ServiceOrder.objects.get(id=order_id)
            if serviceorder.can_cancel:
                serviceorder.status = '2'
                serviceorder.save()
                return redirect('serviceorder_list')
        except models.ServiceOrder.DoesNotExist:
            pass

        return redirect('serviceorder_list')