from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

<<<<<<< HEAD
class Profile:
    def __init__(self, name, email, age):
        self.name = name 
        self.email = email
        self.age = age

profiles = [
    Profile('Austin', 'austin@example.com', 33),
    Profile('Dom', 'Dom@example.com', 28),
    Profile('Diego', 'Diego@example.com', 30),
]
=======
class Profile(models.Model):
    age = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Article(models.Model):
    date = models.DateField()
    content = models.CharField(max_length=3000)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-date']
>>>>>>> 5532d2b9005808a2a0168b6907079b70f3536fad
