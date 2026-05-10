from django.contrib import admin

from .models import Ticket
from .models import PromoCode


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'final_price'
    )


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):

    list_display = (
        'code',
        'discount_percent',
        'active'
    )