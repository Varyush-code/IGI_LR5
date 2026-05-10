from django.db import models
from django.contrib.auth.models import User

class Ticket(models.Model):
    DAY_CHOICES = [
        ('weekday', 'Будний'),
        ('weekend', 'Выходной'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tickets'
    )

    day_type = models.CharField(
        max_length=20,
        choices=DAY_CHOICES
    )

    feeding_show = models.BooleanField(
        default=False,
        verbose_name='Кормление животных'
    )

    active_hours = models.BooleanField(
        default=False,
        verbose_name='Активные часы'
    )

    final_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'{self.user.username}'
    
class PromoCode(models.Model):
    code = models.CharField(
        max_length=50,
        unique=True
    )
    discount_percent = models.PositiveIntegerField()
    active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.code