from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect, render

from payment.views import payment_failed, payment_successful, payment_cancelled
from .views import user_reservation_view, payment_reservation_view

from panel.views import (
    add_class_space_view,
    add_service_view,
    calendar_panel_view,
    edit_class_space_view,
    edit_reservation_view,
    edit_service_view,
    payments_panel_view,
    reservations_panel_view,
    services_panel_view,
    Register_view,
    calendar_show_view,
    recipes,
    recipes_details,
    private_clases,
)
from panel.forms import ReservationForm
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from panel.models import Service


def home_view(request):
    services = Service.objects.all()
    return render(request, "home.html", context={"services": services})


def panel_view(request):
    return render(request, "panel/panel.base.html")


panel_urlpatterns = [
    path("", panel_view, name="panel"),
    path("calendar", calendar_panel_view, name="calendar"),
    path("calendar/space", add_class_space_view, name="add_class_space"),
    path(
        "calendar/space/edit/<int:id>", edit_class_space_view, name="edit_class_space"
    ),
    path("reservations", reservations_panel_view, name="reservations"),
    path("reservations/edit/<int:id>", edit_reservation_view, name="edit_reservation"),
    path("payments", payments_panel_view, name="payments"),
    path("services", services_panel_view, name="services"),
    path("services/add", add_service_view, name="add_service"),
    path("services/edit/<int:service_id>", edit_service_view, name="edit_service"),
]

payment_urlpatterns = [
    path("payment_successful", payment_successful, name="payment_successful"),
    path("payment_failed", payment_failed, name="payment_failed"),
    path("payment_cancelled", payment_cancelled, name="payment_cancelled"),
]

urlpatterns = [
    path("recipes/", recipes, name="recipes"),
    path("recipes/details/", recipes_details, name="recipes_details"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("calendar", calendar_show_view, name="calendar_show"),
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
    path("", home_view, name="home"),
    path("recipes/", recipes, name="recipes"),
    path("recipes/details/", recipes_details, name="recipes_details"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("private-class/", private_clases, name="private"),
    path("calendar", calendar_show_view, name="calendar_show"),
    path("register/", Register_view, name="register"),
    path("logout/", lambda request: redirect("panel:panel"), name="logout"),
    path("admin/", admin.site.urls),
    path("reservation", user_reservation_view, name="reservation"),
    path(
        "reservation/<int:reservation_id>/payment",
        payment_reservation_view,
        name="reservation_payment",
    ),
    path("panel/", include((panel_urlpatterns, "panel"), namespace="panel")),
    path("", home_view, name="home"),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
