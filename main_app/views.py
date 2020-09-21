from django.shortcuts import render, redirect

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DeleteView, ListView 

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Profile, Article, Photo
from django.contrib.auth.models import User

from django import forms
from social_django.utils import load_strategy
import uuid
import boto3
import requests 
import json
from django.http import JsonResponse

import tweepy


S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'teamadd'


def add_photo(request, profile_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, profile_id=profile_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', profile_id=profile_id)

def twitter(request):
    consumer_key = 'dVsH4M3DPLwqtvylzNCCxrZ4d'
    consumer_secret = 'hprfHGgPuM8Oxx5VoMW0GHOZuyCWk4slKn6DTsboV58xfIUfXm'
    access_token = '2319705902-NIvQW965NHgKBsJUIDZlKIRmg6WxZdrXOSvdCQD'
    access_token_secret = 'VCNYaAyxFz2WDjXOLXlyg2pwsjIeeTi5r3zZ3Oty7QUQE'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, 'http://localhost:8000/')
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    twitter_text = {}

    if 'twitter_text' in request.GET:
        twitter_text = request.GET['twitter_text']
        tweet = twitter_text
        api.update_status(status=tweet)

    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        print(tweet.text)
    return render(request, 'core/twitter.html', {"public_tweets": public_tweets})
   
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
    elif 'name' in request.POST:
        name = request.POST['name']
        social = request.user.social_auth.values_list()
        #print(social)
        # print(((social[0])[4])['login'])
        # print(((social[0])[4])['access_token'])
        # url = 'https://api.github.com/user/repos'
        # headers = {}
        payload = { 'name': name }
        # response = requests.post('https://api.github.com/user/repos', data=payload, headers=headers)
        token = ((social[0])[4])['access_token']
        github_user = ((social[0])[4])['login']
        response= requests.post('https://api.github.com/' + 'user/repos', auth=(github_user, token), data=json.dumps(payload))
        print(response)
    return render(request, 'core/github.html', {'search_result': search_result, 'repolist': repolist})
      

    
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def profiles_index(request):
    profiles = Profile.objects.filter(user=request.user)
    return render(request, 'profiles/index.html', {'profiles': profiles})

@login_required
def profiles_detail(request, profile_id):
    profile = Profile.objects.get(id=profile.user.id)
    return render(request, 'profiles/detail.html', { 'profile': profile })


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

class ProfileCreate(LoginRequiredMixin, CreateView):
    model = Profile
    fields = ['bio', 'location', 'age']
    # model = User
    # fields = [user.first_name, user.last_name, user.email]
    def form_valid(self, form):
        form.instance.user = self.request.user  
        return super().form_valid(form)

class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['bio', 'location', 'age']   
   

class ProfileDelete(LoginRequiredMixin, DeleteView):
    model = Profile
    success_url = '/profiles/'

@login_required   
def articles_index(request):
    articles = Article.objects.all()
    return render(request, 'articles/index.html', { 'articles': articles })

@login_required
def articles_detail(request, article_id):
    article = Article.objects.get(id=article_id)
    return render(request, 'articles/detail.html', { 'article': article })

class ArticleCreate(LoginRequiredMixin, CreateView):
    model = Article
    fields = '__all__'

class ArticleUpdate(LoginRequiredMixin, UpdateView):
    model = Article
    fields = '__all__'

class ArticleDelete(LoginRequiredMixin, DeleteView):
    model = Article
    success_url = '/articles/'
