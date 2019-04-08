from django.db import models
from django.contrib.auth.models import AbstractUser
from taggit.managers import TaggableManager
# Create your models here.
class CustomUser(AbstractUser):
    is_customer = models.BooleanField(default='False')
    is_restaurant = models.BooleanField(default='False')
    phone = models.CharField(max_length=12, unique=True)
    avatar = models.FileField(default='images/avatar/unkwown.png', upload_to='images/avatar/')
    choice_category = (('Cu', 'Customer'), ('Re', 'Restaurant'))
    type = models.CharField(max_length=2, choices=choice_category)

class Restaurant(models.Model):
    customuser = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='customuser')
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=12, unique=True)
    address = models.CharField(max_length=50)
    description = models.TextField()
    kind_of_restaurant = models.CharField(max_length=20, blank=True)
    likes = models.ManyToManyField(CustomUser, related_name='likes', blank=True)


class ImagesRestaurant(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    image = models.FileField(upload_to='images/restaurant/')


class Food(models.Model):
    name = models.CharField(max_length=50)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    detail = models.TextField()
    tags = TaggableManager()
    price = models.IntegerField()
    rates = models.ManyToManyField(CustomUser, through='Rate', blank=True)
    score = models.IntegerField(default=0)


class Rate(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    customuser = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    point = models.IntegerField()

class ImagesFood(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    image = models.FileField(upload_to='images/food/')