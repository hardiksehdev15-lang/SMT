from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils.timezone import now
from django.apps import apps

from sehdev.models import MachineEnquiry, EnquiryAttachment
from sehdev.forms import MachineEnquiryForm
# Create your views here.
def enquiry_view(request):
    # 1. URL se product ka naam pakadna (e.g., ?product=Rotary Table)
    product_name = request.GET.get('product', '')

    # ---------- GET ----------
    if request.method == "GET":
        # 2. Form ko pre-fill karke bhejna
        form = MachineEnquiryForm(initial={'other_machinery': product_name})
        return render(request, "enquiry.html", {"form": form})

    # ---------- POST ----------
    form = MachineEnquiryForm(request.POST, request.FILES)
    if not form.is_valid():
        return render(request, "enquiry.html", {"form": form})

    enquiry = form.save()

    # small helper (pretty print)
    def fmt(v):
        if v is None: return ""
        if isinstance(v, list): return ", ".join(map(str, v))
        return str(v)

    # --------- Email body (TEXT) ----------
    lines = [
        "New enquiry received",
        f"Date: {now().strftime('%Y-%m-%d %H:%M')}",
        "",
        f"Name: {fmt(enquiry.full_name)}",
        f"Email: {fmt(enquiry.email)}",
        f"Phone: {fmt(enquiry.phone)}",
        f"Company: {fmt(enquiry.company)}",
        f"City/Country: {fmt(enquiry.city)} / {fmt(enquiry.country)}",
        "",
        # Service Type handle logic (if empty)
        f"Service Type: {enquiry.get_service_type_display() if enquiry.service_type else 'Product Specific Enquiry'}",
        f"Source: {fmt(enquiry.source_service)}",
        f"Machinery Interested: {fmt(getattr(enquiry, 'machinery', []))}",
        f"Other/Specific Product: {fmt(enquiry.other_machinery)}",
        "",
        "Project Details:",
        fmt(enquiry.project_details or ""),
        "",
    ]

    # --------- Conditional Sections ----------
    if enquiry.service_type == 'customization':
        lines.extend([
            "---- Design Customization ----",
            f"Line type: {fmt(enquiry.cust_line_type)}",
            f"Throughput: {fmt(enquiry.cust_throughput)}",
            f"Format: {fmt(enquiry.cust_format)}",
            f"Pain points: {fmt(enquiry.cust_pain_points)}",
            f"PLC/HMI: {fmt(enquiry.cust_plc)}",
            f"Integration: {fmt(enquiry.cust_integration)}",
            f"Deadline: {fmt(enquiry.cust_deadline)}",
            "",
        ])
    elif enquiry.service_type == 'reverse':
        lines.extend([
            "---- Reverse Engineering ----",
            f"Part: {fmt(enquiry.rev_part)}",
            f"Qty: {fmt(enquiry.rev_qty)}",
            f"Sample available: {fmt(enquiry.rev_sample)}",
            f"Material: {fmt(enquiry.rev_material)}",
            f"Operating conditions: {fmt(enquiry.rev_conditions)}",
            f"Drawings available: {fmt(enquiry.rev_docs)}",
            f"Tolerance: {fmt(enquiry.rev_tolerance)}",
            f"Urgency: {fmt(enquiry.rev_urgency)}",
            "",
        ])
    elif enquiry.service_type == 'refurbishment':
        lines.extend([
            "---- Product Refurbishment ----",
            f"Machine Name: {fmt(enquiry.refurb_machine_name)}",
            f"Condition: {fmt(enquiry.refurb_condition)}",
            f"Year: {fmt(enquiry.refurb_year)}",
            f"Notes: {fmt(enquiry.refurb_notes)}",
            "",
        ])

    # attachments handling
    uploaded_files = request.FILES.getlist("attachments")
    if uploaded_files:
        lines.append("Attachments:")
        for f in uploaded_files:
            lines.append(f" - {getattr(f, 'name', 'file')}")
        lines.append("")

    # Email Setup
    service_label = enquiry.get_service_type_display() if enquiry.service_type else "Product"
    subject = f"New Enquiry – {enquiry.full_name} [{service_label}]"
    sender = getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@example.com")
    recipients = ["sehdev02@yahoo.com"]

    email = EmailMessage(subject, "\n".join(lines), sender, recipients)

    for f in uploaded_files:
        email.attach(f.name, f.read(), getattr(f, "content_type", "application/octet-stream"))

    try:
        email.send(fail_silently=False)
    except Exception:
        pass

    # Save to DB (Optional)
    try:
        AttachmentModel = apps.get_model(app_label="sehdev", model_name="EnquiryAttachment")
        if AttachmentModel:
            for f in uploaded_files:
                if hasattr(f, "seek"): f.seek(0)
                obj = AttachmentModel(enquiry=enquiry)
                obj.file.save(f.name, f, save=True)
    except LookupError:
        pass

    return redirect("success_view", enquiry_id=enquiry.id)    


def success_view(request, enquiry_id):
    try:
        enquiry = MachineEnquiry.objects.get(id=enquiry_id)
    except MachineEnquiry.DoesNotExist:
        enquiry = None
    return render(request, 'success.html', {'enquiry': enquiry})



