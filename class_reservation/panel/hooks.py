from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.views.decorators.csrf import csrf_exempt
import os
from django.dispatch import receiver

from django.contrib.auth.models import User
from panel.models import Reservation
from payment.models import ReservationPayment
from utils.mailers import email_admin, email_client


@receiver(valid_ipn_received)
def update_payment_db(sender, **kwargs):
    print("first ipn receiver")
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        if ipn_obj.receiver_email != os.environ.get(
            "PAYPAL_RECEIVER_EMAIL", "sb-47rpes28754189@business.example.com"
        ):
            # Not a valid payment
            return
        # Undertake some action depending upon `ipn_obj`.
        if ipn_obj.custom["type"] == "reservation":
            reservation_id = ipn_obj.custom["reservation"]
            reservation = Reservation.objects.get(id=reservation_id)
            create_payment_entry(reservation, ipn_obj)
            send_user_email(reservation)
            send_admin_email(reservation)


@csrf_exempt
@receiver(valid_ipn_received)
def webhook(sender, **kwargs):
    print("second ipn receiver")
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        if ipn_obj.receiver_email != os.environ.get(
            "PAYPAL_RECEIVER_EMAIL", "sb-47rpes28754189@business.example.com"
        ):
            # Not a valid payment
            return
        # Undertake some action depending upon `ipn_obj`.
        if ipn_obj.custom["type"] == "reservation":
            reservation_id = ipn_obj.custom["reservation"]
            reservation = Reservation.objects.get(id=reservation_id)
            create_payment_entry(reservation, ipn_obj)
            send_user_email(reservation)
            send_admin_email(reservation)


def create_payment_entry(reservation_id, user_id, ipn_obj):
    reservation = Reservation.objects.get(id=reservation_id)
    user = User.objects.get(id=user_id)
    ReservationPayment.objects.create(
        amount=ipn_obj.mc_gross,
        user=user,
        reservation=reservation,
        invoice_id=ipn_obj.invoice,
        payment_name=ipn_obj.item_name,
    )
    return


def send_user_email(reservation):

    context = {"reservation": reservation}
    email_client(
        subject=f"Reservation confirmation",
        body="payment/templates/email/client_msg_for_reservation.html",
        to_email=reservation.email,
        ctx=context,
        html="payment/templates/email/client_msg_for_reservation.html",
    )
    return


def send_admin_email(reservation):

    context = {"reservation": reservation}
    email_admin(
        ctx=context,
        body="payment/templates/email/admin_msg_for_reservation.txt",
        html="payment/templates/email/admin_msg_for_reservation.html",
        subject=f"New Reservation",
    )
