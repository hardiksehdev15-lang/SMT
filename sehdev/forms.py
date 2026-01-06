from django import forms
from .models import MachineEnquiry

class MachineEnquiryForm(forms.ModelForm):
    MACHINERY_CHOICES = [
        ('Labelling Machines', 'Labelling Machines'),
        ('Sealing Machines', 'Sealing Machines'),
        ('Filling Machines', 'Filling Machines'),
        ('Capping Machines', 'Capping Machines'),
        ('Packaging Lines', 'Packaging Lines'),
        ('Ancillary Units', 'Ancillary Units'),

        ('Conveyors', 'Conveyors'),
        ('Spare Parts', 'Spare Parts'),
        ('Nozzles & Needles', 'Nozzles & Needles'),

        ('Mechanical Seals', 'Mechanical Seals'),
        ('Change Parts', 'Change Parts'),
        # ------------------------------------
        ('Other', 'Other'),
    ]

    machinery_ui = forms.MultipleChoiceField(
        choices=MACHINERY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Machinery (select one or more)"
    )

    # honeypot (optional)
    website = forms.CharField(required=False, widget=forms.TextInput(attrs={
        "autocomplete":"off","tabindex":"-1","style":"position:absolute;left:-9999px;"
    }))

    class Meta:
        model = MachineEnquiry
        fields = [
            "full_name","company","email","phone","city","country",
            "machinery_ui","other_machinery","project_details",
            "service_type","source_service",
            # customization
            "cust_line_type","cust_throughput","cust_format","cust_pain_points",
            "cust_plc","cust_integration","cust_deadline",
            # reverse
            "rev_part","rev_qty","rev_sample","rev_material",
            "rev_conditions","rev_docs","rev_tolerance","rev_urgency",
            # refurbishment
            "refurb_machine_name", "refurb_condition", "refurb_year", "refurb_notes",
            "attachment",
            "consent",
        ]
        widgets = {
            "project_details": forms.Textarea(attrs={"rows":4}),
            "cust_pain_points": forms.Textarea(attrs={"rows":3}),
            "refurb_notes": forms.Textarea(attrs={"rows":3}),
            # ✅ Changed: Added an empty option at the top for optional selection
            "service_type": forms.Select(choices=[('', '--- Select Service (Optional) ---')] + [
                ("general","General"),
                ("customization","Design Customization"),
                ("reverse","Reverse Engineering"),
                ("refurbishment","Product Refurbishment"),
            ]),
            "source_service": forms.HiddenInput(),
            "attachment": forms.ClearableFileInput(),
        }

    def __init__(self, *args, **kwargs):
        initial_machinery = kwargs.pop("initial_machinery", None)
        super().__init__(*args, **kwargs)
        
        if self.instance and getattr(self.instance, "machinery", None):
            self.fields["machinery_ui"].initial = list(self.instance.machinery)
        elif initial_machinery:
            self.fields["machinery_ui"].initial = initial_machinery

        # ✅ Added: Explicitly make service_type optional
        if 'service_type' in self.fields:
            self.fields['service_type'].required = False

        # Make all conditional fields non-required so the form submits
        conditional_fields = (
            "cust_line_type","cust_throughput","cust_format","cust_pain_points",
            "cust_plc","cust_integration","cust_deadline",
            "rev_part","rev_qty","rev_sample","rev_material",
            "rev_conditions","rev_docs","rev_tolerance","rev_urgency",
            "refurb_machine_name", "refurb_condition", "refurb_year", "refurb_notes",
            "other_machinery"
        )
        
        for f in conditional_fields:
            if f in self.fields:
                self.fields[f].required = False

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("website"):
            raise forms.ValidationError("Spam detected.")
        cleaned["machinery"] = cleaned.get("machinery_ui") or []
        return cleaned

    def clean_consent(self):
        consent = self.cleaned_data.get("consent")
        if not consent:
            raise forms.ValidationError("You must accept the consent to proceed.")
        return consent

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.machinery = self.cleaned_data.get("machinery", [])
        if commit:
            obj.save()
        return obj