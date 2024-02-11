from django.contrib import admin

from .models import (
    Reservation,
    Service,
    ClassSpaceModel,
    Receta,
    Item_of_recipe,
    Part_of_reciept,
    Preparation,
    Preparation_time_item,
)


# Register your models here.
admin.site.register(Reservation)
admin.site.register(Service)
admin.site.register(Item_of_recipe)
admin.site.register(Receta)
admin.site.register(Part_of_reciept)
admin.site.register(Preparation)
admin.site.register(Preparation_time_item)
admin.site.register(ClassSpaceModel)
