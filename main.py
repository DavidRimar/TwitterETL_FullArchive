import requests
import os
import json
from TweetCollector_FullArchiveAPI import TweetStreamer
from config import *

# tweetStreamer object
tweetStreamer = TweetStreamer(BEARER_TOKEN, DATABASE_URI_TRIAL)

# GET tweets with tweetStreamer
# It also handles data loading to DB via its tweetLoader
# set recreate_db = True if ran for the first time or need to recreate schema
# specify maximum number of tweets to return
tweetStreamer.get_tweets(recreate_db=False, maxTweets=10)
