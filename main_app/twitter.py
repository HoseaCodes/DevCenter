from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
# import .env


TWITTER_API_KEY = "dVsH4M3DPLwqtvylzNCCxrZ4d"
TWITTER_SECRET__KEY = "hprfHGgPuM8Oxx5VoMW0GHOZuyCWk4slKn6DTsboV58xfIUfXm"
TWITTER_ACCESS_TOKEN = "2319705902-NIvQW965NHgKBsJUIDZlKIRmg6WxZdrXOSvdCQD"
TWITTER_ACCESS_TOKEN_SECRET = "VCNYaAyxFz2WDjXOLXlyg2pwsjIeeTi5r3zZ3Oty7QUQE"

class TwitterClient():
    def __int__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for firend in Cursor(self.twitter_client.firends, id=self.twitter_user).items(num_friends):
            friend_list.append(firend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets


class TwitterAuthenticator():
    def authenticate_twitter_app(self):
        auth = OAuthHandler(TWITTER_API_KEY, TWITTER_SECRET__KEY)
        auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
        return auth

class TwitterStreamer():
    def __int__(self):
        self.twitter_authenicator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # auth = OAuthHandler(env.TWITTER_API_KEY, env.TWITTER_SECRET__KEY)
        # auth.set_access_token(env.TWITTER_ACCESS_TOKEN, env.TWITTER_ACCESS_TOKEN_SECRET)
        listner = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_authenicator.authenticate_twitter_app()
        stream = Stream(auth, listner)
        stream.filter(track=hash_tag_list)

class TwitterListener(StreamListener):

    def __int__(se1f, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print('Error on_data:' % str(e))
        return True

    def on_error(self, status):
        if status == 420:
            return false
        print(status)

if __name__ == "__main__":
    hash_tag_list = ['SERI 629, junior software engineer, software engineer intern, coding interview ']
    fetched_tweets_filename = 'tweets.json'

    twitter_client = TwitterClient()
    print(twitter_client.get_user_timeline_tweets(1))
    # twitterstreamer = TwitterStreamer()
    # twitter streamer.stream tweets(fetched_tweets_filename, hash_tag_list)


    # auth = OAuthHandler(TWITTER_API_KEY, TWITTER_SECRET__KEY)
    # auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    # # auth = OAuthHandler(env.TWITTER_API_KEY, env.TWITTER_SECRET__KEY)
    # # auth.set_access_token(env.TWITTER_ACCESS_TOKEN, env.TWITTER_ACCESS_TOKEN_SECRET)
    # listner = StdOutListener()
    # stream = Stream(auth, listner)
    # stream.filter(track=['junior software developers'])
