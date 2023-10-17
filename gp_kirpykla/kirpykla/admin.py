from django.contrib import admin
from . import models


class ServiceOrderAdmin(admin.ModelAdmin):
    list_display = ("barber", "service_name", "customer", "service_time", "created_at")
    list_filter = ("barber", "service")
    list_display_links = ("barber", )
    search_fields = ("serviceorder__barber", "serviceorder__service")
    readonly_fields = ("id", )

    def service_name(self, obj):
        return obj.service.name
    service_name.short_description = "Service Name"

class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "duration", "about")
    list_filter = ("name", "price")
    list_display_links = ("name", )
    search_fields = ("service__name", )
    readonly_fields = ("id", )

class AboutUsAdmin(admin.ModelAdmin):
    list_display = ("content", )
    

@admin.register(models.BarberReview)
class BarberReviewAdmin(admin.ModelAdmin):
    list_display = ('barber', 'reviewer', 'created_at')
    list_display_links = ('created_at', )


admin.site.register(models.ServiceOrder, ServiceOrderAdmin)
admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.AboutUs, AboutUsAdmin)

