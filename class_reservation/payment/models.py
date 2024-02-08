from django.db import models
import random
import string
from django.contrib.auth.models import User
import datetime
from panel.models import Reservation

# Create your models here.

# there will be multiple types of payments
# create abstract class to house them all
# Types of payment = [reservation,class] append to list for more payment types


def generate_unique_invoice_id():
    """Generate a unique invoice ID."""
    unique_id = "invoice-" + "".join(
        random.choices(string.ascii_letters + string.digits, k=32)
    )
    # Check if the generated ID already exists in the database
    while Payment.objects.filter(invoice_id=unique_id).exists():
        unique_id = "invoice-" + "".join(
            random.choices(string.ascii_letters + string.digits, k=32)
        )
    return unique_id


class Payment(models.Model):
    amount = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    invoice_id = models.CharField(
        null=False,
        blank=False,
        max_length=50,
        unique=True,
    )
    payment_name = models.CharField(null=False, blank=False, max_length=50)
    date = models.DateTimeField(auto_now_add=True)


class ReservationPayment(Payment):
    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
    )
