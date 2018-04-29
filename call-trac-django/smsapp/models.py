from django.db import models

# Create your models here.

class MobleNumber(models.Model):
	phone = models.CharField(max_length=20)
	name = models.CharField(max_length=120)

class MobleMessage(models.Model):
	number = models.ForeignKey(MobleNumber, on_delete=models.CASCADE)
	body = models.CharField(max_length=160)
	sent = models.BooleanField()
	date_time = models.DateTimeField(auto_now=True)