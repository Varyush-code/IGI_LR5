from django.db import models

class Openings(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название',
        default='неизвестно'
    )

    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )

    def __str__(self):
        return self.name