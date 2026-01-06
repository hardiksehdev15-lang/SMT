from django.urls import path
from . import views

urlpatterns = [
    path("", views.enquiry_view, name="enquiry"),
    path("success/<int:enquiry_id>/", views.success_view, name="success_view"),
]
