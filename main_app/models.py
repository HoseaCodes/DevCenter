from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

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