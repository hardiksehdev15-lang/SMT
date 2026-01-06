from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils.timezone import now
from django.apps import apps

from .models import (
    MachineEnquiry,EnquiryAttachment
)
from .forms import MachineEnquiryForm


def home_view(request):
    return render(request, 'home.html')

def aboutus_view(request):
    return render(request, 'aboutus.html')

def contactus_view(request):
    return render(request, 'contactus.html')

def services_view(request):
    return render(request, 'services.html')


