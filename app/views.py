from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404
from .form import RegisterForm
from .models import Banner, Timg, Destination, Cont, Gallery, Booking,Payment


import qrcode
import base64
from io import BytesIO
from decimal import Decimal
from urllib.parse import urlencode
from django.http import JsonResponse
from django.db import OperationalError, ProgrammingError
from django.db import OperationalError, ProgrammingError
from django.contrib.auth.decorators import login_required



def home(request):
    ba = []
    t = []

    try:
        ba = Banner.objects.all()
        t = Timg.objects.all()
    except (OperationalError, ProgrammingError):
        print("DB not ready")

    return render(request, 'index.html', {'ba': ba, 'timg': t})

def destination(request):
    dest = Destination.objects.all()

    category = request.GET.get('type', 'all')
    search = request.GET.get('search')

    if category != 'all':
        dest = dest.filter(category__iexact=category)

    if search:
        dest = dest.filter(
            Q(title__icontains=search) |
            Q(category__icontains=search)
        )

    for d in dest:
        d.desc = [x.strip() for x in d.description.split('/')] if d.description else []
        d.pi = [x.strip() for x in d.includes.split('/')] if d.includes else []

    return render(request, 'Destinations.html', { 'dest': dest})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'reg.html', {'form': form})



def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        if request.user.is_authenticated and not request.user.is_superuser:
            Cont.objects.create(
                user=request.user,
                name=name,
                email=email,
                phone=phone,
                message=message
            )
        else:
            Cont.objects.create(
                name=name,
                email=email,
                phone=phone,
                message=message
            )

        messages.success(request, 'Message sent successfully!')
        return redirect('contact')

    return render(request, 'contact.html')


def fbooking(request):
    return render(request, 'info/booking.html')


def privacy(request):
    return render(request, 'info/privacy.html')


def terms(request):
    return render(request, 'info/terms.html')

def about(request):
    return render(request, 'about.html')

def booking_history(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to view your bookings.")
        return redirect('login')

    bookings = Booking.objects.filter(user=request.user).order_by('-id')
    return render(request, 'booking_history.html', {'bookings': bookings})


def booking(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        destination = request.POST.get("destination")
        duration = request.POST.get("duration")
        vehicle_type = request.POST.get("vehicle_type")
        guests = int(request.POST.get("guests", 1))
        price_per_head = Decimal(request.POST.get("price_per_head", "0.00"))
        total_amount = Decimal(guests) * price_per_head

        booking = Booking.objects.create(
            user=request.user if request.user.is_authenticated else None,
            name=name,
            email=request.user.email if request.user.is_authenticated else email,
            destination=destination,
            duration=duration,
            vehicle_type=vehicle_type,
            guests=guests,
            price_per_head=price_per_head,
            total_amount=total_amount
        )

        return redirect('payment', booking_id=booking.id)

    return render(request, 'booking.html')


def payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    qr_code_base64 = None
    error = None

    total_amount = Decimal(str(booking.total_amount)).quantize(Decimal("0.00"))
    selected_amount = total_amount

    if request.method == "POST":
        payment_type = request.POST.get("payment_type")
        payment_method = request.POST.get("payment_method")
        upi_app = request.POST.get("upi_app")
        payment_screenshot = request.FILES.get("payment_screenshot")

        if payment_type == "advance":
            selected_amount = (total_amount * Decimal("0.02")).quantize(Decimal("0.00"))
        else:
            selected_amount = total_amount

        # AJAX QR generation without reload
        if "generate_qr" in request.POST:
            if not payment_type:
                return JsonResponse({"error": "Please select payment type."})

            if not payment_method:
                return JsonResponse({"error": "Please select payment method."})

            if payment_method != "UPI":
                return JsonResponse({"error": "Only UPI payment is available."})

            upi_id = "6383559277@axl"
            payee_name = "Travel Booking"

            upi_params = {
                "pa": upi_id,
                "pn": payee_name,
                "am": str(selected_amount),
                "cu": "INR",
                "tn": f"Booking #{booking.id} payment"
            }

            upi_url = "upi://pay?" + urlencode(upi_params)

            qr = qrcode.make(upi_url)
            buffer = BytesIO()
            qr.save(buffer, format="PNG")
            qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()

            return JsonResponse({
                "qr_code": qr_code_base64,
                "amount": str(selected_amount)
            })

        # Final payment submit
        if not payment_type:
            error = "Please select payment type."
        elif not payment_method:
            error = "Please select payment method."
        elif payment_method != "UPI":
            error = "Only UPI payment is available."
        elif not upi_app:
            error = "Please choose UPI app."
        elif not payment_screenshot:
            error = "Please upload payment screenshot."
        else:
            payment_obj, created = Payment.objects.update_or_create(
                booking=booking,
                defaults={
                    "amount": selected_amount,
                    "payment_method": payment_method,
                    "upi_app": upi_app,
                    "payment_status": "Success",
                    "QR": payment_screenshot
                }
            )

            return redirect("success", payment_id=payment_obj.id)

    return render(request, "payment.html", {
        "booking": booking,
        "qr_code_base64": qr_code_base64,
        "selected_amount": selected_amount,
        "error": error,
    })


def success(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)

    return render(request, "success.html", {
        "payment": payment
    })





def gallery(request):
    gallery_type = request.GET.get('type')

    if gallery_type and gallery_type != 'all':
        gallery_items = Gallery.objects.filter(category=gallery_type)
    else:
        gallery_items = Gallery.objects.all()

    context = {
        'gallery': gallery_items
    }
    return render(request, 'gallery.html', context)




    
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit



def download_statement(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    booking = payment.booking

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Colors
    primary = HexColor("#0d6efd")
    dark = HexColor("#1f2937")
    gray = HexColor("#6b7280")
    light = HexColor("#f3f4f6")
    green = HexColor("#16a34a")

    # Background
    pdf.setFillColor(light)
    pdf.rect(0, 0, width, height, fill=1, stroke=0)

    # Header
    pdf.setFillColor(primary)
    pdf.rect(0, height - 90, width, 90, fill=1, stroke=0)

    pdf.setFillColor(HexColor("#ffffff"))
    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawString(40, height - 50, "UD-Traveler Payment Statement")

    pdf.setFont("Helvetica", 11)
    pdf.drawString(40, height - 70, "Tamil Nadu Premium Travel Booking Receipt")

    # Section title
    y = height - 130
    pdf.setFillColor(dark)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(40, y, "Payment Summary")

    # Line
    pdf.setStrokeColor(primary)
    pdf.setLineWidth(1)
    pdf.line(40, y - 8, width - 40, y - 8)

    y -= 35

    details = [
        ("Booking ID", str(booking.id)),
        ("Customer Name", str(booking.name)),
        ("Email", str(getattr(booking, "email", ""))),
        ("Destination", str(booking.destination)),
        ("Duration", str(getattr(booking, "duration", ""))),
        ("Vehicle Type", str(getattr(booking, "vehicle_type", ""))),
        ("Guests", str(booking.guests)),
        ("Price / Head", f"₹{getattr(booking, 'price_per_head', 0)}"),
        ("Total Booking Amount", f"₹{booking.total_amount}"),
        ("Paid Amount", f"₹{payment.amount}"),
        ("Payment Method", str(payment.payment_method)),
        ("UPI App", str(getattr(payment, "upi_app", ""))),
        ("Payment Status", str(payment.payment_status)),
    ]

    box_x = 40
    box_y = y - 290
    box_w = width - 80
    box_h = 320

    pdf.setFillColor(HexColor("#ffffff"))
    pdf.setStrokeColor(HexColor("#d1d5db"))
    pdf.roundRect(box_x, box_y, box_w, box_h, 12, fill=1, stroke=1)

    text_y = y
    for label, value in details:
        pdf.setFillColor(gray)
        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawString(60, text_y, f"{label}:")

        pdf.setFillColor(dark)
        pdf.setFont("Helvetica", 11)

        wrapped_lines = simpleSplit(str(value), "Helvetica", 11, 280)
        line_y = text_y
        for line in wrapped_lines:
            pdf.drawString(220, line_y, line)
            line_y -= 14

        text_y = line_y - 8

    # Status message
    pdf.setFillColor(green)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(40, box_y - 30, "Payment completed successfully.")

    pdf.setFillColor(gray)
    pdf.setFont("Helvetica", 10)
    pdf.drawString(40, box_y - 48, "Thank you for booking with UD-Traveler.")

    # Footer
    pdf.setFillColor(primary)
    pdf.rect(0, 0, width, 50, fill=1, stroke=0)

    pdf.setFillColor(HexColor("#ffffff"))
    pdf.setFont("Helvetica", 10)
    pdf.drawString(40, 20, "UD-Traveler | Premium Tamil Nadu Travel")

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    filename = f"payment_statement_booking_{booking.id}.pdf"

    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


@login_required
def profile(request):
    user = request.user
    bookings = Booking.objects.filter(email=user.email).order_by('-id')

    first_letter = user.username[0].upper() if user.username else "U"

    return render(request, 'profile.html', {
        'bookings': bookings,
        'first_letter': first_letter,
    })