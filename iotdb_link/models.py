from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.

class Device(models.Model):
    device_name = models.CharField(max_length=200)
    parking_slot = models.IntegerField()
    def __str__(self):
        return str(self.device_name)

class DataFromDevice(models.Model):
    device = models.ForeignKey(Device)
    time = models.DateTimeField(default=timezone.now)
    data = models.CharField(max_length=100, default=0)
    def __str__(self):
        return str(self.time)


