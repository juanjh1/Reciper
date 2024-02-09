from django.shortcuts import render
from django.urls import reverse
import os
from paypal.standard.forms import PayPalPaymentsForm

# Create your views here.


# def process_payment(request):

#     # What you want the button to do.
#     paypal_dict = {
#         "business": "receiver_email@example.com",
#         "amount": "10000000.00",
#         "item_name": "name of the item",
#         "invoice": "unique-invoice-id",
#         "notify_url": request.build_absolute_uri(reverse("paypal-ipn")),
#         "return": request.build_absolute_uri(reverse("your-return-view")),
#         "cancel_return": request.build_absolute_uri(reverse("your-cancel-view")),
#     }

#     # Create the instance.
#     form = PayPalPaymentsForm(initial=paypal_dict)
#     context = {"form": form}
#     return render(request, "checkout/checkout.html", context)


def payment_cancelled(request):
    return render(request, "response/payment_cancelled.html")


def payment_successful(request):
    return render(request, "response/payment_successful.html")


def payment_failed(request):
    return render(request, "response/payment_failed.html")
