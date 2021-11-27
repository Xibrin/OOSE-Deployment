from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    address1 = models.CharField(max_length=200, default="")
    city = models.CharField(max_length=200, default="")
    state = models.CharField(max_length=200, default="")
    country = models.CharField(max_length=200, default="")
    music = models.IntegerField(null=True, default=3, validators=[MinValueValidator(1), MaxValueValidator(5)])
    visual = models.IntegerField(null=True, default=3, validators=[MinValueValidator(1), MaxValueValidator(5)])
    performing = models.IntegerField(null=True, default=3, validators=[MinValueValidator(1), MaxValueValidator(5)])
    film = models.IntegerField(null=True, default=3, validators=[MinValueValidator(1), MaxValueValidator(5)])
    lectures = models.IntegerField(null=True, default=3, validators=[MinValueValidator(1), MaxValueValidator(5)])
    fashion = models.IntegerField(null=True, default=3, validators=[MinValueValidator(1), MaxValueValidator(5)])
    food = models.IntegerField(null=True, default=3, validators=[MinValueValidator(1), MaxValueValidator(5)])
    festivals = models.IntegerField(null=True, default=3, validators=[MinValueValidator(1), MaxValueValidator(5)])
    charity = models.IntegerField(null=True, default=3, validators=[MinValueValidator(1), MaxValueValidator(5)])
    sports = models.IntegerField(null=True, default=3, validators=[MinValueValidator(1), MaxValueValidator(5)])
    nightlife = models.IntegerField(null=True, default=3, validators=[MinValueValidator(1), MaxValueValidator(5)])
    family = models.IntegerField(null=True, default=3, validators=[MinValueValidator(1), MaxValueValidator(5)])


class Event(models.Model):
    name = models.CharField(max_length=200, default="")
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    duration = models.DurationField(null=True, blank=True)
    category = models.CharField(max_length=200, default="")
    picture = models.URLField(max_length=300, null=True, blank=True)
    tickets = models.URLField(max_length=300, null=True, blank=True)
    cost = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    address1 = models.CharField(max_length=200, default="")
    city = models.CharField(max_length=100, default="")
    state = models.CharField(max_length=2, default="")
    country = models.CharField(max_length=100, default="")
    zip_code = models.CharField(max_length=5, default="")
    attendees = models.ManyToManyField("User", related_name="attending")

    def __str__(self):
        return f"Event {self.id}: {self.name}"

    def __hash__(self):
        return hash(self.name)