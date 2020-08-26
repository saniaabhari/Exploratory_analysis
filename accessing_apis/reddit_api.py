# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv
import praw
load_dotenv(override=True)


reddit = praw.Reddit(client_id=os.getenv('reddit_personal_use'),
                     client_secret=os.getenv('reddit_api_key'),
                     user_agent=os.getenv('reddit_app_name'),
                     username=os.getenv('reddit_username'),
                     password=os.getenv('reddit_pw'))

print(reddit.user.me())
subreddit = reddit.subreddit("Coronavirus").top("week")
# subreddit = reddit.subreddit('Coronavirus')
# top_subreddit = subreddit.top()
top_subreddit = subreddit.top(limit=10)

for submission in subreddit.top(limit=20):
    print(submission.title, submission.id)

for submission in top_subreddit:
    topics_dict["title"].append(submission.title)