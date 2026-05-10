from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    text = models.TextField(
        verbose_name='Текст отзыва'
    )

    rating = models.IntegerField(
        choices=RATING_CHOICES,
        verbose_name='Оценка'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'{self.user.username} - {self.rating}'