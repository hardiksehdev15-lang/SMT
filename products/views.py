from django.shortcuts import render
from sehdev.models import (
    LabellingMachine, SealingMachine, FillingMachine, Misc,
    Ancillaryunits, Nozzles, Mechanicalseals,
    Rubbercomponents, Conveyorsystems, WashingUnit,
    LabellingComponent, SealingComponent, FillingComponent,
    ConveyorComponent, Needles, ChangeParts,
    PharmaTool, ConveyorBelt, WearStrip,
    BottleHandlingFixture, WashingComponent, SealingHead
)

# Create your views here.
def products(request):
    return render(request, "products.html")


# ---------- product list views (unchanged) ----------
def LabellingMachine_view(request):
    machines = LabellingMachine.objects.order_by('-created_at')

    components = LabellingComponent.objects.all() 
    
    # Dono variables ko dictionary (context) mein pass karein
    return render(request, 'LabellingMachine.html', {
        'machines': machines,
        'components': components
    })
def SealingMachine_view(request):
    machines = SealingMachine.objects.all().order_by('-created_at')
    components = SealingComponent.objects.all().order_by('-created_at')
    sealing_heads = SealingHead.objects.all().order_by('-created_at') 
    
    context = {
        'machines': machines,
        'components': components,
        'sealing_heads': sealing_heads,
    }
    return render(request, 'SealingMachine.html', context)

def FillingMachine_view(request):
    machines = FillingMachine.objects.all().order_by('-created_at')
    components = FillingComponent.objects.all().order_by('-created_at')
    
    context = {
        'machines': machines,
        'components': components,
    }
    return render(request, 'FillingMachine.html', context)

def Conveyorsystems_view(request):
    machines = Conveyorsystems.objects.all().order_by('-created_at')
    components = ConveyorComponent.objects.all().order_by('-created_at')
    belts = ConveyorBelt.objects.all().order_by('-created_at')
    wear_strips = WearStrip.objects.all().order_by('-created_at') # Naya query
    
    context = {
        'machines': machines,
        'components': components,
        'belts': belts,
        'wear_strips': wear_strips, # Context mein add kiya
    }
    return render(request, 'ConveyorSystems.html', context)

def Misc_view(request):
    machines = Misc.objects.all().order_by('-created_at')
    
    pharma_tools = PharmaTool.objects.all().order_by('-created_at') # Make sure model name is correct
    
    context = {
        'machines': machines,
        'pharma_tools': pharma_tools
    }
    
    return render(request, 'misc.html', context)

def Ancillaryunits_view(request):
    machines = Ancillaryunits.objects.order_by('-created_at')
    return render(request, 'Ancillaryunits.html', {'machines': machines})

def washing_units_view(request):
    machines = WashingUnit.objects.all().order_by('-created_at')
    # Fetch the new components data
    components = WashingComponent.objects.all().order_by('-created_at')
    
    return render(request, 'washing_units.html', {
        'machines': machines,
        'components': components
    })
def Nozzles_view(request):
    nozzle_items = Nozzles.objects.order_by('-created_at')
    needle_items = Needles.objects.order_by('-created_at')
    
    context = {
        'nozzles': nozzle_items,
        'needles': needle_items,
    }
    
    return render(request, 'Nozzles.html', context)

def Mechanicalseals_view(request):
    machines = Mechanicalseals.objects.order_by('-created_at')
    return render(request, 'Mechanicalseals.html', {'machines': machines})

def ChangeParts_view(request):
    machines = ChangeParts.objects.all().order_by('-created_at')
    fixtures = BottleHandlingFixture.objects.all().order_by('-created_at')
    
    return render(request, 'Change_Parts.html', {
        'machines': machines,
        'fixtures': fixtures
    })

def Rubbercomponents_view(request):
    machines = Rubbercomponents.objects.order_by('-created_at')
    return render(request, 'Rubbercomponents.html', {'machines': machines})

