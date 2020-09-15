from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

# Create your models here.

class Article(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateField()
    content = models.CharField(max_length=3000)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('articles_detail', kwargs={'article_id': self.id})

    class Meta:
        ordering = ['-date']


class Profile(models.Model):
    age = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    articles = models.ManyToManyField(Article)

    def __str__(self):
        return self.name
    
