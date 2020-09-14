from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required



# Create your views here.
class Profile():
    def __init__(self, name, email, age):        
        self.name = name 
        self.email = email
        self.age = age

profiles = [
    Profile('Austin', 'austin@example.com', 33),
    Profile('Dom', 'Dom@example.com', 28),
    Profile('Diego', 'Diego@example.com', 30),
]

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def profiles_index(request):
    return render(request, 'profiles/index.html', {'profiles': profiles})

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)