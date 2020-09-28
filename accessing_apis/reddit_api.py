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

# ------------------------------------------------- USING PUSHSHIFT -------------------------------------------------

from psaw import PushshiftAPI

# Uses pushshift search to fetch ids and then uses praw to fetch objects
# 'reddit' was defined in line 11 using praw and the users personal api key and other information
api = PushshiftAPI(reddit)


start_epoch=int(dt.datetime(2020, 9, 23).timestamp())
end_epoch=int(dt.datetime(2020, 9, 25).timestamp())
result = api.search_submissions(after=start_epoch,
                            subreddit='politics',
                            filter=['url','author', 'title', 'subreddit'],
                            limit=10)

https://api.pushshift.io/reddit/search/comment/?q=trump&after=start_epochd&before=end_epochd&sort=asc
https://api.pushshift.io/reddit/comment/search/?subreddit=politics&q=trump&after=start_epochd&before=end_epochd&sort=asc

https://api.pushshift.io/reddit/comment/search/?subreddit=politics&q=trump&after=1600833600&before=1601006400&sort=asc
https://api.pushshift.io/reddit/comment/search/?subreddit=politics&q=trump&after=1577854800&before=1601006400&sort=asc


https://api.pushshift.io/reddit/search/comment/?q=trump&after=7d&aggs=subreddit&size=0

api = PushshiftAPI()
# The `search_comments` and `search_submissions` methods return generator objects
gen = api.search_submissions(limit=100)
next(gen)
cache = []

for c in gen:
    print(c)
    cache.append(c)

results = list(gen)

start_epoch=int(dt.datetime(2020, 1, 1).timestamp())

list(api.search_submissions(after=start_epoch,
                            subreddit='wallstreetbets',
                            filter=['title','score', 'id', 'url','author','created_utc'],
                            limit=10))


import requests

return requests.get(url).json()
url = "https://api.pushshift.io/reddit/search/submission"
params = {"subreddit": "ifyoulikeblank"}
submissions = requests.get(url, params = params)
type(submissions)
last_submission_time = submissions.json()
params = {"subreddit" : "ifyoulikeblank", "before" : last_submission_time}
submissions = requests.get(url, params = params)