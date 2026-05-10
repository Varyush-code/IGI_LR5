from django.db import models
from apps.animals.models import Animal
from apps.employees.models import Employee

class Food(models.Model):

    FOOD_TYPES = [
        ('meat', 'Мясо'),
        ('fish', 'Рыба'),
        ('grass', 'Трава'),
        ('fruit', 'Фрукты'),
        ('vegetables', 'Овощи'),
    ]

    food_type = models.CharField(
        max_length=50,
        choices=FOOD_TYPES
    )

    def __str__(self):
        return self.food_type
    
class Feeding(models.Model):

    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name='feedings'
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='feedings'
    )

    food = models.ForeignKey(
        Food,
        on_delete=models.CASCADE
    )

    amount = models.PositiveIntegerField()

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.animal} - {self.food}"