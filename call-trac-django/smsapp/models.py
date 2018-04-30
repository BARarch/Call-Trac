from django.db import models

# Create your models here.

class MobileNumber(models.Model):
	phone = models.CharField(max_length=20)
	name = models.CharField(max_length=120)

class MobileMessage(models.Model):
	number = models.ForeignKey(MobileNumber, on_delete=models.CASCADE)
	body = models.CharField(max_length=160)
	sent = models.BooleanField()
	date_time = models.DateTimeField(auto_now=True)