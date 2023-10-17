from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about_us/', views.about_us, name="about_us"),
    path('services/', views.ServiceListView.as_view(), name='service_list'),
    path('services/<int:pk>/order/', views.OrderServiceCreateView.as_view(), name='order_service'),
]