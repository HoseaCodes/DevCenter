from django.contrib import admin

from .models import Profile, Article, Photo
# Register your models here.
admin.site.register(Profile)
admin.site.register(Article)
admin.site.register(Photo)

