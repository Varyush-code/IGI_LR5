from django.contrib import admin
from .models import Food, Feeding

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('food_type',)

@admin.register(Feeding)
class FeedingAdmin(admin.ModelAdmin):

    list_display = ('animal', 'employee', 'food', 'amount', 'date')

    list_filter = ('food', 'employee')