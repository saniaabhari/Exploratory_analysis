# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv
import praw
import pprint
import datetime as dt
load_dotenv(override=True)

# ------------------------------------------------- USING PRAW -------------------------------------------------
reddit = praw.Reddit(client_id=os.getenv('reddit_personal_use'),
                     client_secret=os.getenv('reddit_api_key'),
                     user_agent=os.getenv('reddit_app_name'),
                     username=os.getenv('reddit_username'),
                     password=os.getenv('reddit_pw'))

# View your own username
print(reddit.user.me())

# The two lines below may become useful if you decide to work with dates
# now = dt.datetime.utcnow()
# timestamp = now.timestamp()

subreddit = reddit.subreddit("wallstreetbets").search(query="tesla", sort='new', time_filter='year', limit=1000)
posts = list()
for index, submission in enumerate(subreddit):
    subreddit_output = dict()

    # The submission title
    subreddit_output['title'] = submission.title

    # The net upvotes of the submission
    subreddit_output['score'] = submission.score

    # The submission's ID
    subreddit_output['id'] = submission.id

    # The url of the submission
    subreddit_output['url'] = submission.url

    # All comment id's connected to the submission
    all_comments = submission.comments.list()
    subreddit_output['comments'] = all_comments

    # The username of the submission
    subreddit_output['author'] = submission.author

    # The datetime of the submission
    submission_date = dt.datetime.utcfromtimestamp(submission.created_utc)
    subreddit_output['submission_date'] = submission_date

    # To display all available Attributes of an Object you can uncomment the pprint line
    # and view what other attributes you would want to pull out, example attributes are shown above
    # pprint.pprint(vars(submission))

    # Pretty print the dictionary
    pprint.pprint(subreddit_output)

    # Inserting a submission to the collection in the database
    # collection.insert_one(subreddit_output)
    posts.append(subreddit_output)
