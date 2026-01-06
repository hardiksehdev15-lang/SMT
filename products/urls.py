from django.urls import path
from . import views

urlpatterns = [
    path("", views.products, name="products"),

    path("labelling-machine/", views.LabellingMachine_view, name="LabellingMachine_view"),
    path("sealing-machine/", views.SealingMachine_view, name="SealingMachine_view"),
    path("filling-machine/", views.FillingMachine_view, name="FillingMachine_view"),
    path("ancillary-units/", views.Ancillaryunits_view, name="Ancillaryunits_view"),
    path("washing-units/", views.washing_units_view, name="washing_units_view"),
    path("misc/", views.Misc_view, name="Misc_view"),
    path("nozzles/", views.Nozzles_view, name="Nozzles_view"),
    path("mechanical-seals/", views.Mechanicalseals_view, name="Mechanicalseals_view"),
    path("change-parts/", views.ChangeParts_view, name="ChangeParts_view"),
    path("rubber-components/", views.Rubbercomponents_view, name="Rubbercomponents_view"),
    path("conveyor-systems/", views.Conveyorsystems_view, name="Conveyorsystems_view"),
]
