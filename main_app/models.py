from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

class Article(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateField()
    content = models.TextField(max_length=3000)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('articles_detail', kwargs={'article_id': self.id})

    class Meta:
        ordering = ['-date']

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    age = models.IntegerField()
    bio = models.TextField(max_length=100)
    articles = models.ManyToManyField(Article)

    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         self.name = self.user.first_name + self.user.last_name
    #     super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'profile_id': self.id})
    
class Photo(models.Model):
    url = models.CharField(max_length=200)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    # article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for profile_id: {self.profile_id} @{self.url}"

