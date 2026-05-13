from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):

    ROLE_CHOICES = [
        ('visitor', 'Посетитель'),
        ('employee', 'Работник'),
        ('admin', 'Администратор'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    age = models.DateField(
        null=True, 
        blank=True
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='visitor'
    )

    def __str__(self):
        return self.user.username