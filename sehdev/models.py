from django.db import models
from django import forms


# =========================
#   Core / Real Models
# =========================

from django.db import models

class MachineEnquiry(models.Model):
    # ---------- Contact ----------
    full_name = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    # ---------- Machinery ----------
    machinery = models.JSONField(default=list, blank=True)
    other_machinery = models.TextField(blank=True, null=True)

    # ---------- General ----------
    project_details = models.TextField(blank=True, null=True)

    SERVICE_CHOICES = [
        ('general', 'General Enquiry'),
        ('customization', 'Design Customization'),
        ('reverse', 'Reverse Engineering'),
        ('refurbishment', 'Product Refurbishment'),
    ]
    # Changes: Removed default, added null=True and blank=True
    service_type = models.CharField(
        max_length=32, 
        choices=SERVICE_CHOICES, 
        blank=True, 
        null=True
    )
    source_service = models.CharField(max_length=50, blank=True, null=True)

    # ===== Design Customization specific =====
    cust_line_type = models.CharField(max_length=255, blank=True, null=True)
    cust_throughput = models.CharField(max_length=255, blank=True, null=True)
    cust_format = models.CharField(max_length=255, blank=True, null=True)
    cust_pain_points = models.TextField(blank=True, null=True)
    cust_plc = models.CharField(max_length=255, blank=True, null=True)
    cust_integration = models.CharField(max_length=255, blank=True, null=True)
    cust_deadline = models.CharField(max_length=255, blank=True, null=True)

    # ===== Reverse Engineering specific =====
    REV_YESNO = [('Yes', 'Yes'), ('No', 'No')]
    rev_part = models.CharField(max_length=255, blank=True, null=True)
    rev_qty = models.PositiveIntegerField(blank=True, null=True)
    rev_sample = models.CharField(max_length=3, choices=REV_YESNO, blank=True, null=True)
    rev_material = models.CharField(max_length=255, blank=True, null=True)
    rev_conditions = models.CharField(max_length=255, blank=True, null=True)
    rev_docs = models.CharField(max_length=3, choices=REV_YESNO, blank=True, null=True)
    rev_tolerance = models.CharField(max_length=255, blank=True, null=True)
    rev_urgency = models.CharField(max_length=255, blank=True, null=True)

    # ===== Product Refurbishment specific =====
    refurb_machine_name = models.CharField(max_length=255, blank=True, null=True)
    refurb_condition = models.CharField(max_length=100, blank=True, null=True)
    refurb_year = models.CharField(max_length=50, blank=True, null=True)
    refurb_notes = models.TextField(blank=True, null=True)

    # ---------- Attachment ----------
    attachment = models.FileField(
        upload_to="enquiries/", blank=True, null=True,
        help_text="Upload drawing / photo / reference document"
    )

    # ---------- Meta ----------
    consent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        # Added a fallback in case service_type is empty
        service = self.get_service_type_display() if self.service_type else "Product Enquiry"
        return f"Enquiry {self.id} – {self.full_name} – {service}"

def enquiry_upload_path(instance, filename):
    return f"enquiries/{instance.enquiry_id}/{filename}"


class EnquiryAttachment(models.Model):
    enquiry = models.ForeignKey(MachineEnquiry, related_name='attachments', on_delete=models.CASCADE)
    file    = models.FileField(upload_to='enquiries/%Y/%m')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Attachment {self.id} (Enquiry {self.enquiry_id})"

class LabellingMachine(models.Model):
    name = models.TextField(null=True)
    image = models.ImageField(null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or "Labelling Machine"

class LabellingComponent(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(null=True) 
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class SealingMachine(models.Model):
    name = models.TextField(null=True)
    image = models.ImageField(null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or "Sealing Machine"

class SealingHead(models.Model):
     name = models.TextField(null=True)
     image = models.ImageField(null=True)
     created_at = models.DateTimeField(auto_now=True)


     def __str__(self):
        return self.name
    
class SealingComponent(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class FillingMachine(models.Model):
    name = models.TextField(null=True)
    image = models.ImageField(null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or "Filling Machine"

class FillingComponent(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Misc(models.Model):
    name = models.TextField(null=True)
    image = models.ImageField(null=True, upload_to='products/misc/')
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or "Miscellaneous Item"


class Ancillaryunits(models.Model):
    name = models.TextField(null=True)
    image = models.ImageField(null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or "Ancillary Unit"
    
class WashingUnit(models.Model):
    name = models.TextField(null=True)
    image = models.ImageField(null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class WashingComponent(models.Model):
    name = models.TextField(null=True)
    image = models.ImageField(null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
from django.db import models

class Nozzles(models.Model):
    name = models.TextField(null=True)
    image = models.ImageField(null=True)
    created_at = models.DateTimeField(auto_now=True)
  
    def __str__(self):
        return self.name

class Needles(models.Model):
    name = models.TextField(null=True)
    image = models.ImageField(null=True)
    created_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class Mechanicalseals(models.Model):
    name = models.TextField(null=True)
    image = models.ImageField(null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or "Mechanical Seal"

class ChangeParts(models.Model):
    name = models.TextField(null=True)
    image = models.ImageField(null=True, upload_to='products/change-parts/')
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or "Change Part"

class BottleHandlingFixture(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='fixtures/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
        
class Rubbercomponents(models.Model):
    name = models.TextField(null=True)
    image = models.ImageField(null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or "Rubber Component"


class Conveyorsystems(models.Model):
    name = models.TextField(null=True)
    image = models.ImageField(null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or "Conveyor System"

class ConveyorBelt(models.Model):
    name = models.TextField(null=True)
    image = models.ImageField(null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __clstr__(self):
        return self.name
    
class ConveyorComponent(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(null=True)
    created_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class WearStrip(models.Model):
    name = models.TextField(null=True)
    image = models.ImageField(null=True, upload_to='wear_strips/')
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name if self.name else "Unnamed Wear Strip"
        
class PharmaTool(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
# ==================================================
#   Proxy Models for Clean Admin Grouping (Reliable)
#   → No new DB tables, sirf admin UI grouping
# ==================================================

# --- Enquiries group ---
class MachineEnquiryAdmin(MachineEnquiry):
    class Meta:
        proxy = True
        app_label = "enquiries"
        verbose_name = "Machine enquiry"
        verbose_name_plural = "Machine enquiries"


# --- Products group (proxies for each product model) ---

class LabellingMachineAdmin(LabellingMachine):
    class Meta:
        proxy = True
        app_label = "products"
        verbose_name = "Labelling machine"
        verbose_name_plural = "Labelling machines"


class SealingMachineAdmin(SealingMachine):
    class Meta:
        proxy = True
        app_label = "products"
        verbose_name = "Sealing machine"
        verbose_name_plural = "Sealing machines"


class FillingMachineAdmin(FillingMachine):
    class Meta:
        proxy = True
        app_label = "products"
        verbose_name = "Filling machine"
        verbose_name_plural = "Filling machines"


class AncillaryunitsAdmin(Ancillaryunits):
    class Meta:
        proxy = True
        app_label = "products"
        verbose_name = "Ancillary unit"
        verbose_name_plural = "Ancillary units"


class NozzlesAdmin(Nozzles):
    class Meta:
        proxy = True
        app_label = "products"
        verbose_name = "Nozzle / Needle"
        verbose_name_plural = "Nozzles & Needles"

class MechanicalsealsAdmin(Mechanicalseals):
    class Meta:
        proxy = True
        app_label = "products"
        verbose_name = "Mechanical seal"
        verbose_name_plural = "Mechanical seals"


class RubbercomponentsAdmin(Rubbercomponents):
    class Meta:
        proxy = True
        app_label = "products"
        verbose_name = "Rubber component"
        verbose_name_plural = "Rubber components"


class ConveyorsystemsAdmin(Conveyorsystems):
    class Meta:
        proxy = True
        app_label = "products"
        verbose_name = "Conveyor system"
        verbose_name_plural = "Conveyor systems"