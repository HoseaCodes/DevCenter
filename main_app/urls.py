from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('profiles/', views.profiles_index, name='index'),
    path('profiles/create', views.ProfileCreate.as_view(), name='profiles_create'),
    path('profiles/<int:profile_id>/', views.profiles_detail, name='detail'),
    path('profiles/<int:pk>/update', views.ProfileUpdate.as_view(), name='profiles_update'),
    path('profiles/<int:pk>/delete', views.ProfileDelete.as_view(), name='profiles_delete'),
    path('accounts/signup/', views.signup, name='signup'),
]