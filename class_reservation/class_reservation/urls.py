from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect, render

from django.contrib.auth.decorators import user_passes_test

# Función para verificar si el usuario es superusuario
def is_superuser(user):
    return user.is_superuser

# Decorador para restringir el acceso a las vistas solo a superusuarios
def superuser_required(view_func):
    return user_passes_test(lambda user: is_superuser(user))(view_func)


from payment.views import payment_failed, payment_successful, payment_cancelled
from .views import user_reservation_view, payment_reservation_view, reservation_post

from panel.views import (
    add_class_space_view,
    add_service_view,
    calendar_panel_view,
    desc_service,
    edit_class_space_view,
    edit_reservation_view,
    edit_service_view,
    payments_panel_view,
    profile,
    reservations_panel_view,
    services_panel_view,
    Register_view,
    calendar_show_view,
    recipes,
    recipes_details,
    private_clases,
    desc_service,
    profile, services_view
)

from panel.forms import ReservationForm
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from panel.models import Service


def home_view(request):
    services = Service.objects.all()
    print(services)
    return render(request, "home.html", context={"services": services})


def panel_view(request):
    return render(request, "panel/panel.base.html")

panel_urlpatterns = [
    path("", superuser_required(panel_view), name="panel"),
    path("calendar", superuser_required(calendar_panel_view), name="calendar"),
    path("calendar/space", superuser_required(add_class_space_view), name="add_class_space"),
    path("calendar/space/edit/<int:id>", superuser_required(edit_class_space_view), name="edit_class_space"),
    path("reservations/<int:id>", superuser_required(reservations_panel_view), name="reservations"),
    path("reservations/edit/<int:id>", superuser_required(edit_reservation_view), name="edit_reservation"),
    path("payments", superuser_required(payments_panel_view), name="payments"),
    path("services", superuser_required(services_panel_view), name="services"),
    path("services/add", superuser_required(add_service_view), name="add_service"),
    path("services/edit/<int:service_id>", superuser_required(edit_service_view), name="edit_service"),
]

payment_urlpatterns = [
    path(
        "payment_successful/<int:reservation_id>/<str:invoice_id>",
        payment_successful,
        name="payment_successful",
    ),
    path("payment_failed", payment_failed, name="payment_failed"),
    path("payment_cancelled", payment_cancelled, name="payment_cancelled"),
]

urlpatterns = [
    path("recipes/details/<int:id>", recipes_details, name="recipes_details"),
    path("profile/<int:id>", profile, name="profile"),
    path("service_desc/<int:id>", desc_service, name="service"),
    path("private-class/", private_clases, name="private"),
    path("calendar", calendar_show_view, name="calendar_show"),
    path("recipes/", recipes, name="recipes"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("register/", Register_view, name="register"),
    path("logout/", lambda request: redirect("panel:panel"), name="logout"),
    path("admin/", admin.site.urls),
    path("reservation", user_reservation_view, name="reservation"),
    path(
        "reservation/<int:reservation_id>/payment",
        payment_reservation_view,
        name="reservation_payment",
    ),
    path("paypal/", include("paypal.standard.ipn.urls")),
    path("panel/", include((panel_urlpatterns, "panel"), namespace="panel")),
    path("payment/", include((payment_urlpatterns, "payment"), namespace="payments")),
    path("recipes/", recipes, name="recipes"),
     path("services/", services_view, name="services"),
    path("recipes/details/", recipes_details, name="recipes_details"),
    path("recipes/details/<int:id>", recipes_details, name="recipes_details"),
    path("calendar", calendar_show_view, name="calendar_show"),
    path("register/", Register_view, name="register"),
    path("logout/", lambda request: redirect("panel:panel"), name="logout"),
    path("reservation/<int:id>", user_reservation_view, name="reservation"),
    path("reservation/pay", reservation_post, name="reservation_post"),
    path(
        "reservation/<int:reservation_id>/payment",
        payment_reservation_view,
        name="reservation_payment",
    ),
    path("", home_view, name="home"),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
