from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('profiles/', views.profiles_index, name='index'),
    path('profiles/create', views.ProfileCreate.as_view(), name='profiles_create'),
    path('accounts/signup/', views.signup, name='signup'),
]