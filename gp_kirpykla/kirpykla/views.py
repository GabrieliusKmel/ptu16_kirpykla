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
    template_name = 'service_list.html'
    context_object_name = 'services'



class OrderServiceCreateView(LoginRequiredMixin, CreateView):
    model = models.ServiceOrder
    form_class = forms.ServiceOrderForm
    template_name = 'kirpykla/order_service.html'
    success_url = reverse_lazy('service_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Užsakymas atliktas sėkmingai.')
        return super().form_valid(form)