import random
import string

from payment.models import Payment


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
