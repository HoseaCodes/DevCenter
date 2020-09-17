from django.shortcuts import render, redirect

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DeleteView, ListView 

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic  import DetailView, ListView

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Profile, Article
import json
import requests





def github(request):
    search_result = {}
    repolist = []
    
    if 'username' in request.GET:
        username = request.GET['username']
        url = 'https://api.github.com/users/%s' % username 
        response = requests.get(url)
        search_was_successful = (response.status_code == 200)  # 200 = SUCCESS
        search_result = response.json()
        search_result['success'] = search_was_successful
        search_result['rate'] = {
            'limit': response.headers['X-RateLimit-Limit'],
            'remaining': response.headers['X-RateLimit-Remaining'],
        }
        response = requests.get(search_result['repos_url'])
        repolist = response.json()
    # elif 'fname' in request.GET:
    #     fname = request.GET['fname']
    #     print(f'username: ', fname)
    #     user = social.extra_data['login']
    #     social = user.social_auth.get(provider='oauth')
    #     reponame = request.POST['fname']
    #     access_token = social.extra_data['access_token']
    #     headers = {'access_token': access_token}
    #     response = requests.post('https://api.github.com/user/repos', scope = {'public_repo': public_repo},  data = {'name': reponame}, headers = headers)
    #     # response = requests.post('https://api.github.com/user/Burgosdss/repos?access_token=a4aff9812f4f9a3582457a4f023a2fe91a011015')
    return render(request, 'core/github.html', {'search_result': search_result, 'repolist': repolist})


    # if 'fname' in request.GET:
    #     fname = request.POST('fname')
    #     print(f'username: ', fname)
    #     user = social.extra_data['login']
    #     social = user.social_auth.get(provider='oauth')
    #     reponame = request.POST['fname']
    #     access_token = social.extra_data['access_token']
    #     headers = {'access_token': access_token}
    #     response = requests.post('https://api.github.com/user/repos',  data = {'name': reponame}, headers = headers)
    # return render(request, 'core/create_repo.html', {'repo': repo})  





# Create your views here.
# class Profile():
#     def __init__(self, name, email, age):        
#         self.name = name 
#         self.email = email
#         self.age = age

# profiles = [
#     Profile('Austin', 'austin@example.com', 33),
#     Profile('Dom', 'Dom@example.com', 28),
#     Profile('Diego', 'Diego@example.com', 30),
# ]

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def profiles_index(request):
    profiles = Profile.objects.all()
    # profiles = Profile.objects.filter(user=request.user)
    return render(request, 'profiles/index.html', {'profiles': profiles})

def profiles_detail(request, profile_id):
  profile = Profile.objects.get(id=profile_id)
  return render(request, 'profiles/detail.html', { 'profile': profile })
# def profiles_detail(request, profile_id):
#     profile = Profile.objects.get(id=profile_id)
#     return render(request, 'profiles/detail.html', {
#         'profile': profile,
#     })

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

class ProfileCreate( CreateView):
    model = Profile
    fields = '__all__' 

class ProfileUpdate( UpdateView):
    model = Profile
    fields = ['bio', 'location', 'age']    

class ProfileDelete( DeleteView):
    model = Profile
    success_url = '/profiles/'
    
def articles_index(request):
    articles = Article.objects.all()
    return render(request, 'articles/index.html', { 'articles': articles })

def articles_detail(request, article_id):
    article = Article.objects.get(id=article_id)
    return render(request, 'articles/detail.html', { 'article': article })

class ArticleCreate(CreateView):
    model = Article
    fields = '__all__'

class ArticleUpdate(UpdateView):
    model = Article
    fields = '__all__'

class ArticleDelete(DeleteView):
    model = Article
    success_url = '/articles/'
