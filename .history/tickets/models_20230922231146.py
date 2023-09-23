from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings  # to get the user model (default)


# Guests -- Movie -- Reservation  (عميل بيحجز في فندق)


class Movie(models.Model):
    hall = models.CharField(max_length=10)
    movie = models.CharField(max_length=10)


class Guest(models.Model):
    name = models.CharField(max_length=10)
    mobile = models.CharField(max_length=10)


class Reservation(models.Model):
    guest = models.ForeignKey(
        Guest,
        related_name="reservation",
        on_delete=models.CASCADE,
    )
    movie = models.ForeignKey(
        Movie,
        related_name="reservation",
        on_delete=models.CASCADE,
    )


# signal to make token when the user created
# reciver: to make the token automatically when the user created
# post_save: to make the token after the user created
# sender: to make the token for the user model
@receiver(post_save,sender=settings.AUTH_USER_MODEL) 
def TokenCreate():
    if created:
        Token.objects.create(user=instance)
