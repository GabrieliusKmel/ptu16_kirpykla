from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about_us/', views.about_us, name="about_us"),
    path('services/', views.ServiceListView.as_view(), name='service_list'),
    path('book-service/', views.book_service, name='book_service'),
    path('booking-success/', views.booking_success, name='booking_success'),
]