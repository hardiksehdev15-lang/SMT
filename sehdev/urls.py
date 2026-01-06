from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("home/", views.home_view, name="home"),

    path("home/aboutus/", views.aboutus_view, name="aboutus_view"),
    path("home/contactus/", views.contactus_view, name="contactus_view"),
    path("home/services/", views.services_view, name="services_view"),

]
