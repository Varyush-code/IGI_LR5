from django.db import models

class Enclosure(models.Model):
    TYPE_CHOICES = [
        ('savanna', 'Саванна'),
        ('aquarium', 'Аквариум'),
        ('jungle', 'Джунгли'),
        ('forest', 'Лес'),
    ]

    number = models.IntegerField(
        verbose_name='Номер'
    )

    name = models.CharField(
        max_length=100,
        verbose_name='Название вольера'
    )

    enclosure_type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        verbose_name='Тип вольера',
        default=1
    )

    capacity = models.IntegerField(
        default=1,
        verbose_name='Вместимость'
    )

    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Вольер'
        verbose_name_plural = 'Вольеры'