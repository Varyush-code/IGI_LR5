from django.db import models
import logging
from apps.enclosures.models import Enclosure
from apps.employees.models import Employee

class Animal(models.Model):
    GENDER_CHOICES = [
        ('male', 'Самец'),
        ('female', 'Самка'),
    ]

    name = models.CharField(
        max_length=100,
        verbose_name='Имя',
        default='неизвестно'
    )

    species = models.CharField(
        max_length=100,
        verbose_name='Вид',
        default='неизвестно'
    )

    family = models.CharField(
        max_length=100,
        verbose_name='Семейство',
        default='неизвестно'
    )

    age = models.IntegerField(
        default=0,
        verbose_name='Возраст'
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        verbose_name='Пол',
        default='male'
    )

    country = models.CharField(
        max_length=100,
        verbose_name='Страна происхождения',
        default='неизвестно'
    )

    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )

    image = models.ImageField(
        upload_to='animals/',
        blank=True,
        null=True,
        verbose_name='Фото'
    )

    arrival_date = models.DateField(
        auto_now_add=True,
        verbose_name='Дата поступления'
    )

    enclosure = models.ForeignKey(
        Enclosure,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='animals',
        verbose_name='Вольер'
    )

    employee = models.ManyToManyField(
        Employee,
        blank=True,
        related_name='animals',
        verbose_name='Смотрители'
    )

    def __str__(self):
        return f'{self.name} - {self.species}'

    class Meta:
        verbose_name = 'Животное'
        verbose_name_plural = 'Животные'
        ordering = ['name']
