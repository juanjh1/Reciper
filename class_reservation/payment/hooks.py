from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.views.decorators.csrf import csrf_exempt
import os
from django.dispatch import receiver

from django.contrib.auth.models import User
from panel.models import Reservation
from payment.models import ReservationPayment


def update_payment_db(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:

        if ipn_obj.receiver_email != os.environ.get(
            "PAYPAL_RECEIVER_EMAIL", "sb-47rpes28754189@business.example.com"
        ):
            # Not a valid payment
            return

        # Undertake some action depending upon `ipn_obj`.
        if ipn_obj.custom["type"] == "reservation":
            create_payment_entry(
                ipn_obj.custom["reservation"], ipn_obj.custom["user"], ipn_obj
            )

        return


update_payment_db.connect(update_payment_db)


@csrf_exempt
@receiver(valid_ipn_received)
def webhook(sender, **kwargs):
    ipn_obj = sender
    print(f"webhook ::: {ipn_obj}")
    if ipn_obj.payment_status == ST_PP_COMPLETED:

        if ipn_obj.receiver_email != os.environ.get(
            "PAYPAL_RECEIVER_EMAIL", "sb-47rpes28754189@business.example.com"
        ):
            # Not a valid payment
            return

        # Undertake some action depending upon `ipn_obj`.
        if ipn_obj.custom["type"] == "reservation":
            create_payment_entry(
                ipn_obj.custom["reservation"], ipn_obj.custom["user"], ipn_obj
            )

        return
    return


def create_payment_entry(reservation_id, user_id, ipn_obj):
    reservation = Reservation.objects.get(id=reservation_id)
    user = User.objects.filter(id=user_id)
    ReservationPayment.objects.create(
        amount=ipn_obj.mc_gross,
        user=user,
        reservation=reservation,
        invoice_id=ipn_obj.invoice,
        payment_name=ipn_obj.item_name,
    )
    return
