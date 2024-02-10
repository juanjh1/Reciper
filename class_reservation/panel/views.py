import datetime
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ClassSpaceEditForm, ClassSpaceForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import ClassSpaceModel, Service
from .forms import ServiceForm
from panel.models import ClassSpaceModel, Reservation, Service, Receta, Part_of_reciept, Item_of_recipe
from django.contrib.auth import authenticate, login


# ------------------------
# Calendar Views
# ------------------------
def calendar_panel_view(request):
    class_spaces = ClassSpaceModel.objects.all()

    class_spaces_by_day = {
        'Monday': [],
        'Tuesday': [],
        'Wednesday': [],
        'Thursday': [],
        'Friday': [],
        'Saturday': [],
        'Sunday': [],
    }
    past_class_spaces = []
    for class_space in class_spaces:
        # class_spaces_by_day[class_space.day].append(class_space)
        # class_spaces_by_day[class_space["day"]].append(class_space)
        if class_space.week_cyclic != True and class_space.day < datetime.date.today():
            past_class_spaces.append(class_space)
            continue
        day_name = class_space.day.strftime('%A')
        class_spaces_by_day[day_name].append(class_space)
    return render(request, 'panel/calendar.html', context={"class_spaces_by_day": class_spaces_by_day, "past_class_spaces": past_class_spaces})


def add_class_space_view(request):
    if request.method == 'POST':
        form = ClassSpaceForm(request.POST)
        breakpoint()
        if form.is_valid():
            form.save()
            url = reverse('panel:calendar')
            return redirect(url)
    else:
        form = ClassSpaceForm()
    return render(request, 'panel/calendar.space.form.html', {'form': form})

def edit_class_space_view(request, id):
    class_space = ClassSpaceModel.objects.get(id=id)
    if request.method == 'POST':
        form = ClassSpaceEditForm(request.POST, instance=class_space)
        if form.is_valid():
            form.save()
            url = reverse('panel:calendar')
            return redirect(url)
    else:
        form = ClassSpaceEditForm(instance=class_space)
    return render(request, 'panel/calendar.space.edit.html', {'form': form})


# ------------------------
# Services Views
# ------------------------


def services_panel_view(request):
    """View that shows the main services panel.

    Services panel allows to create, and modify different
    services to offer. Each service may have different
    characteristics like price per item,
    discount codes (amount or percentage),
    description and location.

    This panel is used to show the options in
    the reservation form. The services that are
    active here, are the ones that allow to take reservations.
    """
    services = Service.objects.all()
    return render(request, 'panel/services.html', context={"services": services})

def add_service_view(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            url = reverse('panel:services')
            return redirect(url)
    else:
        form = ServiceForm()

    return render(request, 'panel/services.add.html', {'form': form})


def edit_service_view(request, service_id):
    """
    View that allows to edit a service.
    """
    service = Service.objects.get(id=service_id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            url = reverse('panel:services')
            return redirect(url)
    else:
        form = ServiceForm(instance=service)
    return render(request, 'panel/services.edit.html', context={"service": service})


# ------------------------
# Reservation Views
# ------------------------


def reservations_panel_view(request):
    reservations = Reservation.objects.all()

    return render(request, 'panel/reservations.html', {'reservations': reservations})


def edit_reservation_view(request, id):
    reservation = Reservation.objects.get(id=id)

    return render(request, 'panel/reservations.edit.html', context={"reservation": reservation})


# ------------------------
# Payment Views
# ------------------------

def payments_panel_view(request):
    payments = Reservation.objects.filter(status='Paid')
    return render(request, 'panel/payments.html', context={"payments": payments})



# ------------------------
# Register view
# ------------------------

def  Register_view(request):
    
    if request.method == "POST":
       
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        nombre = request.POST['nombre']
        apellido  =   request.POST['apellido']
        user = User.objects.create_user(username=username, password=password, email=email)
        user.first_name = nombre
        user.last_name = apellido
        user.save()
        
        authenticated_user = authenticate(request, username=username, password=password)
        if authenticated_user:
            login(request, authenticated_user)

        return  redirect('/')


# ------------------------
# calendar view
# ------------------------


def calendar_show_view(request):
    
    return render( request, 'calendar_dates.html')

# ------------------------
# recipes view
# ------------------------

def recipes (request):
     
    context = {
        "recipes": Receta.objects.all(),
     

    }
    return render( request, 'recipes.html',context=context)

# ------------------------
# recipes details view
# ------------------------


def recipes_details (request, id ):


    recipe = Receta.objects.filter(id=id).first()
    print( Part_of_reciept.objects.filter(recipe = id))
    print(Item_of_recipe.objects.all())
    context = {
        "recipe":recipe ,
        "recipes_items": Part_of_reciept.objects.filter(recipe = id),
        'ingredients': Item_of_recipe.objects.all()

    }

   
    return render( request, 'recipes_details.html', context=context)


# ------------------------
# view of 
# ------------------------


def private_clases(request, ):

    return render( request, 'private_class.html')




# ------------------------
# view of profile
# ------------------------


def profile (request, id):

    user = User.objects.filter(id=id).first()

    return render( request, 'profile.html')



# ------------------------
# view of profile
# ------------------------


def  desc_service (request, id):

    user = User.objects.filter(id=id).first()

    return render( request, 'class_des.html')



