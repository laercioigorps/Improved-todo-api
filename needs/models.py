from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

class Need(models.Model):
	name = models.CharField(max_length=30)
	description = models.CharField(max_length=80, default='')
	user = models.ForeignKey(User, on_delete =models.CASCADE)

class Goal(models.Model):
	name = models.CharField(max_length=30)
	description = models.CharField(max_length=80, default='')
	endDate = models.DateField(default=date.today())
	need = models.ForeignKey(Need, on_delete=models.CASCADE)

class Step(models.Model):
	name = models.CharField(max_length=30)
	description = models.CharField(max_length=80, default='')
	completed = models.BooleanField(default=False)
	goal = models.ForeignKey(Goal, on_delete=models.CASCADE)

