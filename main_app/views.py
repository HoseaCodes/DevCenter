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
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from decouple import config



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

# def article_add_photo(request, article_id):
#     photo_file = request.FILES.get('photo-file', None)
#     if photo_file:
#         s3 = boto3.client('s3')
#         key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
#         try:
#             s3.upload_fileobj(photo_file, BUCKET, key)
#             url = f"{S3_BASE_URL}{BUCKET}/{key}"
#             photo = Photo(url=url, article_id=article_id)
#             photo.save()
#         except:
#             print('An error occurred uploading file to S3')
#     return redirect('articles_detail', article_id=article_id)



def twitter(request):
    consumer_key = config('CONSUMER_KEY')
    consumer_secret = config('CONSUMER_SECRET')
    access_token = config('ACCESS_TOKEN')
    access_token_secret = config('ACCESS_TOKEN_SECRET')

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

class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return render(request, 'core/twitter.html', {"tweets": tweets})


    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return render(request, 'core/twitter.html', {"friend_list": friend_list})


    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return render(request, 'core/twitter.html', {"home_timeline_tweets": home_timeline_tweets})


# # # # TWITTER AUTHENTICATER # # # #
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth

# # # # TWITTER STREAMER # # # #
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self):
        self.twitter_autenticator = TwitterAuthenticator()    

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_autenticator.authenticate_twitter_app() 
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords: 
        stream.filter(track=hash_tag_list)


# # # # TWITTER STREAM LISTENER # # # #
class TwitterListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True
          
    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs.
            return False
        print(status)

 
if __name__ == '__main__':
 
    # Authenticate using config.py and connect to Twitter Streaming API.
    hash_tag_list = ["junior software engineer", "software engineer intern", "SEIR 629"]
    fetched_tweets_filename = "tweets.txt"

    twitter_client = TwitterClient('')
    print(twitter_client.get_user_timeline_tweets(1))



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

@login_required
def profiles_index(request):
    print(request)
    profiles = Profile.objects.filter(user=request.user)
    return render(request, 'profiles/index.html', {'profiles': profiles})

@login_required
def profiles_detail(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
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
    fields = ['name','bio', 'location', 'age']
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
    return render(request, 'articles/index.html', { 
        'articles': articles,
         })

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
