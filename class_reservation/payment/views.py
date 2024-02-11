from django.shortcuts import render
from django.urls import reverse
import os
from paypal.standard.forms import PayPalPaymentsForm
from panel.models import Reservation
from payment.models import ReservationPayment
from background_task import background
from utils.mailers import email_admin, email_client

# Create your views here.


def payment_cancelled(request):
    return render(request, "response/payment_cancelled.html")


def payment_successful(request, reservation_id, invoice_id):
    print("payment successful ")
    # reservation_id = request.GET.get("reservation_id")
    # invoice_id = request.GET.get("invoice_id")
    reservation = Reservation.objects.get(id=reservation_id)
    create_payment_entry(reservation_id, request, invoice_id)
    send_user_email(reservation)
    send_admin_email(reservation)
    print("payment successful completed ")
    return render(request, "response/payment_successful.html")


def payment_failed(request):
    return render(request, "response/payment_failed.html")


# @background(schedule=0)
def create_payment_entry(reservation_id, request, invoice_id):
    reservation = Reservation.objects.get(id=reservation_id)
    ReservationPayment.objects.get_or_create(
        amount=reservation.service.price * reservation.tickets,
        user=request.user,
        reservation=reservation,
        invoice_id=invoice_id,
        payment_name=f"{reservation.service.name} : {reservation.class_space.day} : {reservation.class_space.start_time} - {reservation.class_space.end_time}",
    )
    return


# @background(schedule=0)
def send_user_email(reservation):

    context = {
        "reservation": reservation,
        "total": reservation.service.price * reservation.tickets,
    }
    email_client(
        subject=f"Reservation confirmation",
        body="email/client_msg_for_reservation.html",
        to_email=(reservation.email,),
        ctx=context,
        html="email/client_msg_for_reservation.html",
    )
    return


# @background(schedule=0)
def send_admin_email(reservation):

    context = {"reservation": reservation}
    email_admin(
        ctx=context,
        body="email/admin_msg_for_reservation.txt",
        html="email/admin_msg_for_reservation.html",
        subject=f"New Reservation",
    )
