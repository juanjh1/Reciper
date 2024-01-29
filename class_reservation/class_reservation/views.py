import datetime
from django.shortcuts import redirect, render
from panel.models import ClassSpaceModel, Reservation, Service
from panel.forms import PaymentForm, ReservationForm


def user_reservation_view(request):
    """
    View to allow users to make a reservation completing the
    reservation form.
    """
    services = Service.objects.all()
    # Filter spaces available in the future
    spaces_available = ClassSpaceModel.objects.filter(space_type='ONLINE', 
                                                      day__gte=datetime.date.today())
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        breakpoint()
        if form.is_valid():
            form.save()
            return redirect('reservation_payment', form.instance.id)
        else:
            return render(request, 'reservation_form.html', {'form': form, "services": services, "spaces": spaces_available})
    else:
        form = ReservationForm()
    return render(request, 'reservation_form.html', {'form': form, 'services': services, "spaces": spaces_available})


def payment_reservation_view(request, reservation_id):
    """
    View to allow users to make a payment completing the
    payment form.
    """
    reservation = Reservation.objects.get(id=reservation_id)
    # breakpoint()
    total_cost = reservation.service.price * reservation.tickets
    data = {'name': reservation.name, 'email': reservation.email, 'phone_number': reservation.phone_number,
            'service': str(reservation.service), 'class_space': reservation.class_space, 'tickets': reservation.tickets,
            'total_cost': total_cost}
    # Change reservation status to paid
    # if everything is ok

    # if request.method == 'POST':

    return render(request, 'panel/payment_form.html', {'reservation_data': data})
