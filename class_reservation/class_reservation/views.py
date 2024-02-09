import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from class_reservation.utils import generate_unique_invoice_id
from panel.models import ClassSpaceModel, Reservation, Service
from panel.forms import PaymentForm, ReservationForm
import os
from paypal.standard.forms import PayPalPaymentsForm


def user_reservation_view(request):
    """
    View to allow users to make a reservation completing the
    reservation form.
    """
    services = Service.objects.all()
    # Filter spaces available in the future
    spaces_available = ClassSpaceModel.objects.filter(
        space_type="ONLINE", day__gte=datetime.date.today()
    )
    if request.method == "POST":
        form = ReservationForm(request.POST)
        # breakpoint()
        if form.is_valid():
            form.save()
            return redirect("reservation_payment", form.instance.id)
        else:
            return render(
                request,
                "reservation_form.html",
                {"form": form, "services": services, "spaces": spaces_available},
            )
    else:
        form = ReservationForm()
    return render(
        request,
        "reservation_form.html",
        {"form": form, "services": services, "spaces": spaces_available},
    )


def payment_reservation_view(request, reservation_id):
    """
    View to allow users to make a payment completing the
    payment form.
    """
    reservation = Reservation.objects.get(id=reservation_id)
    # breakpoint()
    total_cost = reservation.service.price * reservation.tickets
    data = {
        "name": reservation.name,
        "email": reservation.email,
        "phone_number": reservation.phone_number,
        "service": str(reservation.service),
        "class_space": reservation.class_space,
        "tickets": reservation.tickets,
        "total_cost": total_cost,
    }
    invoice_id = generate_unique_invoice_id()
    paypal_dict = {
        "business": os.environ.get(
            "PAYPAL_RECEIVER_EMAIL", "sb-47rpes28754189@business.example.com"
        ),
        "amount": f"{total_cost}",
        "currency_code": os.environ.get("PAYPAL_CURRENCY_CODE", "USD"),
        "item_name": f"{reservation.service.name} : {reservation.class_space.day} : {reservation.class_space.start_time} - {reservation.class_space.end_time}",
        "invoice": invoice_id,
        "notify_url": request.build_absolute_uri(reverse("paypal-ipn")),
        "return": request.build_absolute_uri(reverse("payments:payment_successful")),
        "cancel_return": request.build_absolute_uri(
            reverse("payments:payment_successful")
        ),
        "custom": {"type": "reservation", id: reservation_id, "user": request.user.id},
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    # Change reservation status to paid
    # if everything is ok

    # if request.method == 'POST':

    return render(
        request, "panel/payment_form.html", {"reservation_data": data, "form": form}
    )
