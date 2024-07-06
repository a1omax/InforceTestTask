import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from restaurants.models import Menu, Restaurant


class Employee(AbstractUser):
    # Additional data about employee may be here
    def __str__(self):
        return f"{self.username}"


class Vote(models.Model):
    user = models.ForeignKey("Employee", on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name="Restaurant")
    date = models.DateField(verbose_name="Date", auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'restaurant', 'date'], name='unique_vote')
        ]

    def __str__(self):
        return f"{self.user.username} - {self.restaurant.name}"

