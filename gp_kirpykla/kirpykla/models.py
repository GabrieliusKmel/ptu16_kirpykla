from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.contrib.auth import get_user_model
from tinymce.models import HTMLField
from datetime import timedelta
from django.contrib.auth.models import User


User = get_user_model()


class Service(models.Model):
    name = models.CharField(_("name"), max_length=50)
    price = models.DecimalField(_("price"), max_digits=18, decimal_places=2)
    duration = models.DurationField(_("duration"), default=timedelta(minutes=30))
    about = HTMLField(_("about"), max_length=10000, default='', blank=True)
    
    class Meta:
        verbose_name = _("service")
        verbose_name_plural = _("services")

    def __str__(self):
        return f"{self.name} {self.price} {self.duration} {self.about}"

    def get_absolute_url(self):
        return reverse("service_detail", kwargs={"pk": self.pk})
    
SERVICEORDER_STATUS = (
    (0, _("confirmed")),
    (1, _("completed")),
    (2, _("cancelled")),
)


class ServiceOrder(models.Model):
    barber = models.ForeignKey(
        User, 
        verbose_name=_("barber"), 
        on_delete=models.CASCADE,
        related_name="jobs",
        null=True,
        blank=True,
    )
    service = models.ForeignKey(
        Service, 
        verbose_name=_("service"), 
        on_delete=models.CASCADE
    )
    customer = models.ForeignKey(
        User, 
        verbose_name=_("customer"), 
        on_delete=models.CASCADE,
        related_name="service_orders",
        )
    status = models.PositiveSmallIntegerField(
        _("status"),
        choices=SERVICEORDER_STATUS, 
        default=0,
    )
    service_time = models.DateTimeField(_("service_time"), null=True, blank=True)
    created_at = models.DateTimeField(_("created_at"), auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = _("service order")
        verbose_name_plural = _("service orders")

    def __str__(self):
        return f"{self.barber} {self.service} {self.customer}"

    def get_absolute_url(self):
        return reverse("serviceorder_detail", kwargs={"pk": self.pk})


class BarberReview(models.Model):
    barber = models.ForeignKey(
        User, 
        verbose_name=_("barber"), 
        on_delete=models.CASCADE,
        related_name="customer_reviews",
    )
    reviewer = models.ForeignKey(
        User, 
        verbose_name=_("reviewer"), 
        on_delete=models.CASCADE,
        related_name='barber_reviews',
    )
    content = models.TextField(_("content"), max_length=4000)
    created_at = models.DateTimeField(
        _("created at"), 
        auto_now_add=True, 
        db_index=True
    )

    class Meta:
        verbose_name = _("barber review")
        verbose_name_plural = _("barber reviews")

    def __str__(self):
        return f"{self.barber} review by {self.reviewer}"

    def get_absolute_url(self):
        return reverse("barberreview_detail", kwargs={"pk": self.pk})


class AboutUs(models.Model):
    content = HTMLField(_("content"), blank=True, null=True)

    class Meta:
        verbose_name = _("about us")
        verbose_name_plural = _("about us")

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse("aboutus_detail", kwargs={"pk": self.pk})