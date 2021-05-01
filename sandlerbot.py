#!/usr/bin/python3

import os
import time
import tweepy
import urllib3
from bs4 import BeautifulSoup

consumer_key = os.environ.get('CONSUMER_KEY')
consumer_secret = os.environ.get('CONSUMER_SECRET')
access_key = os.environ.get('ACCESS_KEY')
access_secret = os.environ.get('ACCESS_SECRET')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

api = tweepy.API(auth)

url = "https://subslikescript.com/movie/Click-389860"
http_pool = urllib3.connection_from_url(url)
r = http_pool.urlopen('GET',url)

response = r.data

soup = BeautifulSoup(response, features="html.parser")

# kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()  # rip it out

# get text
text = soup.get_text()

# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
text = '\n'.join(chunk for chunk in chunks if chunk).split("\n")
del text[0:10]
line_num = 0

user = 'kingAdamSandler'
print(text)
# Getting data for user kingAdamSandler
item = api.get_user(user)

# Prints number of statuses for user
number_of_tweets = item.statuses_count


def send_click_tweet():
    num = number_of_tweets
    tweet_content = text[num]
    if len(text[num]) < 280:
        api.update_status(tweet_content)
    else:
        tweet_content = tweet_content.split(".")
        tweet_content = tweet_content[0] + "." + tweet_content[1] + "."
        api.update_status(tweet_content)


while True:
    send_click_tweet()
    time.sleep(86400)


