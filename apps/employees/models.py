from django.db import models
from apps.accounts.models import Profile
from django.core.validators import RegexValidator

class Employee(models.Model):

    phone_regex = RegexValidator(
        regex=r'^\+375 \(\d{2}\) \d{3}-\d{2}-\d{2}$',
        message='Номер телефона должен быть в формате: +375 (29) XXX-XX-XX'
    )

    name = models.CharField(
        max_length=100,
        verbose_name='Имя',
        default='неизвестно'
    )

    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name='employee_data'
    )

    phone = models.CharField(
        max_length=20,
        validators=[phone_regex],
        verbose_name='Телефон',
        help_text='Формат: +375 (29) XXX-XX-XX'
    )

    description = models.TextField(
        blank=True
    )

    photo = models.ImageField(
        upload_to='employees/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name
    