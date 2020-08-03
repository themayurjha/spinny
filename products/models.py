from django.db import models
from django.contrib.auth.models import User
from datetime import date
# Create your models here.
class Box(models.Model):
    length = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    area = models.FloatField()
    volume = models.FloatField()
    created_by = models.CharField(max_length=100)
    last_updated_date = models.DateField()
    user_id = models.IntegerField()
    creation_date = models.DateField()

class Count(models.Model):
    average_area = models.IntegerField()
    average_volume = models.IntegerField()
    box_added_in_week = models.IntegerField()
    box_added_by_user_in_week = models.IntegerField()


# class Box(models.Model):
#     length = models.IntegerField(default=0)
#     width = models.IntegerField(default=0)
#     height = models.IntegerField(default=0)
#     area = models.FloatField(default=0)
#     volume = models.FloatField(default=0)
#     created_by = models.CharField(max_length=100, default='')
#     last_updated_date = models.DateField(default=date.today())
#     user_id = models.IntegerField(default=0)
#     creation_date = models.DateField(default=date.today())