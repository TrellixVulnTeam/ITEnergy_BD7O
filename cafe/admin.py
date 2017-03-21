from django.contrib import admin

from .models import Product, DeliveryOrder, ReservationOrder, DeliveryStaff, Item


class ItemInline(admin.TabularInline):
    model = Item

class DeliveryOrderAdmin(admin.ModelAdmin):
    inlines = [
        ItemInline,
    ]

admin.site.register(Product)
admin.site.register(DeliveryOrder, DeliveryOrderAdmin)
admin.site.register(ReservationOrder)
admin.site.register(DeliveryStaff)
