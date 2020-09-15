from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    bio = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    age = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'profile_id': self.id})
    
class Article(models.Model):
    date = models.DateField()
    content = models.CharField(max_length=3000)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-date']
