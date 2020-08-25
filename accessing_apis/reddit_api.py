# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv
import praw
load_dotenv()

reddit_key = os.getenv('reddit_api_key')
reddit_username = os.getenv('reddit_username')
reddit_pw = os.getenv('reddit_pw')
reddit_app_name = os.getenv('reddit_app_name')
reddit_personal_use_script = os.getenv('reddit_personal_use')



reddit = praw.Reddit(client_id=reddit_personal_use_script, \
                     client_secret=reddit_key, \
                     user_agent=reddit_app_name, \
                     username=reddit_username, \
                     password=reddit_pw)


subreddit = reddit.subreddit('Coronavirus')
top_subreddit = subreddit.top()
top_subreddit = subreddit.top(limit=10)