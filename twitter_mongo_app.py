# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

# Dash Necessary Imports
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

# User Imports
import pymongo
from datetime import datetime


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Connect to the MongoDB, change the connection string per your MongoDB environment
# Set the db object to point to the tcg database
db = pymongo.MongoClient().tcg
collection = db.ja_tweet

ja_tweets = pd.DataFrame()
for tweet in collection.find():
  if tweet['truncated']==True:
    text = tweet['extended_tweet']['full_text']
  else:
    text = tweet['text']
  tweet_dict = {
      'created_at':tweet['created_at']
      ,'lang':tweet['lang']
      ,'text':text
      ,'user_location':tweet['user']['location']
      ,'user_screenname':tweet['user']['screen_name']
      ,'user_friends_count':tweet['user']['friends_count']
      ,'user_geo_enabled':tweet['user']['geo_enabled']
      }
#  print('\n\n',tweet_dict)
  ja_tweets=ja_tweets.append(tweet_dict, ignore_index=True)

hashtags =['#tradingcards','#sportscards','#whodoyoucollect','#cards','#topps',
           '#tcg','#paniniamerica','#basketballcards','#pokemontcg','#yugioh',
           '#pokemoncards','#footballcards','#yugiohcommunity','#rookiecard',
           '#upperdeck','#tradingcardgame','#baseballcards',
           '#magicthegathering','#cardcollector','#mtg','#psagrade',
           'psa10','#hockeycards','#tradingcard','#cardcollection',
           '#mtgcommunity','#wotc','#yugiohcards','#pokemoncommunity',
           '#yugiohtcg','#sportscardsforsalearthockey','#yugiohcollection',
           '#nbacards','#mtgaddicts','#rookiecards','#donruss',
           '#pokemoncollector','#pokeball','#pokemontrainer',
           '#pokedex','#pokemonswordshield','#pokemonxy',
           '#pokemoncollection','#wizardsofthecoast','#pokemoncard',
           '#pokemonletsgo','#ygo','#pokemontradingcardgame',
           '#swordandshield','#mtgcards','#yugiohcard','#pokemonworld',
           '#yugiohcollector','#ocg','#yugiohzexal','#duellinks',
           '#baseset','#darkmagician','#secretrare','#tcgplayer',
           '#boosterbox','#boosterpack','#pokemontcgcommunity',
           '#rebelclash','#therosbeyonddeath']

# Checking if hashtag was used in text and creating a dataframe containing tag,user,hour of tweet, and friend count
tag = list()
user = list()
created_at = list()
friend_count = list()
for hashtag in hashtags:
  for index,tweet in ja_tweets.iterrows():
    if hashtag in tweet['text'].lower():
      tag.append(hashtag)
      user.append(tweet['user_screenname'])
      friend_count.append(tweet['user_friends_count'])
      converted_created_at = datetime.strftime(datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S')
      created_at.append(converted_created_at)
tagged_tweets = {'tag':tag,'user':user,'created_at':created_at,'friend_count':friend_count}
tagged_tweets_df = pd.DataFrame(tagged_tweets)
tagged_tweets_df['created_at'] = pd.to_datetime(tagged_tweets_df['created_at'])
tagged_tweets_df['created_at_hour'] = tagged_tweets_df['created_at'].dt.hour

# Group by hour and tag
count_tags=tagged_tweets_df.groupby(['created_at_hour','tag'], as_index=False).count()

count_tags_fig = px.line(count_tags, x="created_at_hour", y="created_at",
              color='tag',template="simple_white",
              labels={
                     "created_at_hour": "Time (Hours)",
                     "created_at": "Number of Tweets",
                     "tag": "Trading Card Hashtags"
                 },
                title="Tweet Frequency By Hashtags within a 24 hour Period")
#count_tags_fig.show()

# Number of Users Per Hour By Hashtag
# Dedupe to only keep one row of the set hour,tag,user
deduped_by_hr_tag_id=tagged_tweets_df.drop_duplicates(subset=['created_at_hour', 'tag','user','friend_count'], keep='last')
users_per_hour = deduped_by_hr_tag_id.groupby(['created_at_hour','tag'],as_index=False)['user'].count()

users_per_hour_fig = px.line(users_per_hour, x="created_at_hour", y="user", 
              color='tag',template="simple_white",
              labels={
                     "created_at_hour": "Time (Hours)",
                     "user": "Number of Users",
                     "tag": "Trading Card Hashtags"
                 },
                title="Number of Users Per Hour By Hashtag within a 24 hour Period")
#users_per_hour_fig.show()

# Number of Users Per Hashtag - Grouped By Friend Count
deduped_by_tag_user=tagged_tweets_df.drop_duplicates(subset=['tag','user'], keep='last')
deduped_by_tag_user = deduped_by_tag_user.copy()
bins = [0, 500, 1000,3000,6000, 10000, 20000]
deduped_by_tag_user['binned'] = pd.cut(deduped_by_tag_user['friend_count'], bins)
tags_by_friendcount = deduped_by_tag_user.groupby(['binned','tag'],as_index=False)['user'].count()
#Need to conver to string so I get around the error:
# TypeError: Object of type 'Interval' is not JSON serializable
# for more information check out: https://github.com/altair-viz/altair/issues/1691
tags_by_friendcount.binned = tags_by_friendcount.binned.astype('str').astype('category')

tags_by_friendcount_fig = px.bar(tags_by_friendcount, x="binned", y="user", 
              color='tag',barmode="group",template="simple_white",
              labels={
                     "binned": "Friend Count",
                     "user": "Number of Users",
                     "tag": "Trading Card Hashtags"
                 },
                title="Number of Users Per Hashtag - Grouped By Friend Count within a 24 hour Period")
#tags_by_friendcount_fig.show()

app.layout = html.Div(children=[
    html.H1(children=' Twitter Data of Trading Card Game Tags within 24 Hours'),

    html.Div(children='''
        Language: Japanese.
        Dash Example by: Sania Abhari
    '''),
    dcc.Graph(
        id='graph1',
        figure=count_tags_fig
    )
    ,dcc.Graph(
        id='graph2',
        figure=users_per_hour_fig
    )
    ,dcc.Graph(
        id='graph3',
        figure=tags_by_friendcount_fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
    
    
    
    



