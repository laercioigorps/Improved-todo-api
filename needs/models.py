from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone

# Create your models here.


class Need(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=80, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    iconName = models.CharField(max_length=20, null=True)
    iconColor = models.CharField(max_length=17, null=True)

    def __str__(self):
        return self.name


class Goal(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=80, default='')
    endDate = models.DateField(auto_now_add=False, null=True)
    need = models.ForeignKey(Need, on_delete=models.CASCADE)


class Step(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=80, default='')
    completed = models.BooleanField(default=False)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)


class Iteration(models.Model):
    number = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=False, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class Delivery(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=100)
    step = models.ForeignKey(
        Step, on_delete=models.CASCADE, null=True)  # may be changed
    iteration = models.ForeignKey(
        Iteration, on_delete=models.CASCADE, null=True)
    completed = models.BooleanField(default=False)
