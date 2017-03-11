from django.contrib import admin

from .models import Product, DeliveryOrder, ReservationOrder, DeliveryStaff

admin.site.register(Product)
admin.site.register(DeliveryOrder)
admin.site.register(ReservationOrder)
admin.site.register(DeliveryStaff)
