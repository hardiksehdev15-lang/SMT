from django.contrib import admin
from .models import (
    MachineEnquiry, EnquiryAttachment,
    Misc, LabellingMachine, SealingMachine, FillingMachine,
    Ancillaryunits, Nozzles, Mechanicalseals,
    Rubbercomponents, Conveyorsystems , WashingUnit ,LabellingComponent ,SealingComponent,FillingComponent, ConveyorComponent,Needles,ChangeParts,PharmaTool,ConveyorBelt,WearStrip,BottleHandlingFixture,SealingHead,WashingComponent
)


# Inline to show uploaded attachments
class EnquiryAttachmentInline(admin.TabularInline):
    model = EnquiryAttachment
    extra = 0
    readonly_fields = ("uploaded_at",)


@admin.register(MachineEnquiry)
class MachineEnquiryAdmin(admin.ModelAdmin):
    # ---- List page ----
    list_display = (
        "created_at", "full_name", "email", "phone",
        "company", "service_type", "source_service",
        "machinery_list", "consent",
    )
    list_display_links = ("created_at", "full_name")
    date_hierarchy = "created_at"

    search_fields = (
        "full_name", "email", "company", "phone",
        "project_details", "other_machinery",
        "cust_line_type", "cust_throughput", "cust_format", "cust_pain_points",
        "rev_part", "rev_material", "rev_conditions", "city", "country",
    )

    list_filter = (
        "service_type", "source_service", "consent",
        "created_at", "country", "city",
    )

    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Contact", {
            "fields": (
                ("full_name", "company"),
                ("email", "phone"),
                ("city", "country"),
            )
        }),
        ("Service Context", {
            "fields": ("service_type", "source_service"),
            "description": ""
        }),
        ("Machinery (optional)", {
            "fields": ("machinery", "other_machinery"),
            "description": ""
        }),
        ("Project Details", {
            "fields": ("project_details",),
        }),
        ("Design Customization (optional)", {
            "classes": ("collapse",),
            "fields": (
                "cust_line_type", "cust_throughput", "cust_format",
                "cust_pain_points", "cust_plc", "cust_integration", "cust_deadline"
            ),
        }),
        ("Reverse Engineering (optional)", {
            "classes": ("collapse",),
            "fields": (
                "rev_part", "rev_qty", "rev_sample", "rev_material",
                "rev_conditions", "rev_docs", "rev_tolerance", "rev_urgency"
            ),
        }),
        ("Meta", {
            "fields": ("consent", "created_at", "updated_at"),
        }),
    )

    inlines = [EnquiryAttachmentInline]

    def machinery_list(self, obj):
        if not obj.machinery:
            return "-"
        try:
            return ", ".join(obj.machinery)
        except Exception:
            return str(obj.machinery)
    machinery_list.short_description = "Machinery"


# ---- Product models (simple register) ----
admin.site.register(Misc)
admin.site.register(LabellingMachine)
admin.site.register(SealingMachine)
admin.site.register(FillingMachine)
admin.site.register(Ancillaryunits)
admin.site.register(Nozzles)
admin.site.register(Needles)
admin.site.register(Mechanicalseals)
admin.site.register(Rubbercomponents)
admin.site.register(Conveyorsystems)
admin.site.register(WashingUnit)
admin.site.register(LabellingComponent)
admin.site.register(SealingComponent)
admin.site.register(FillingComponent)
admin.site.register(ConveyorComponent)
admin.site.register(ChangeParts)
admin.site.register(PharmaTool)
admin.site.register(ConveyorBelt)
admin.site.register(WearStrip)
admin.site.register(BottleHandlingFixture)
admin.site.register(SealingHead)
admin.site.register(WashingComponent)




