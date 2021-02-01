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

# Bootstrap Library
import time

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.graph_objs as go
from dash.dependencies import Input, Output

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

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)

app.layout = dbc.Container(
    [
        dcc.Store(id="store"),
        html.H1("Twitter Data of Trading Card Game Tags within 24 Hours"),
        html.P("Language: Japanese. \n Dash Example by: Sania Abhari ",
            className="lead",
        ),
        html.Hr(),
        dbc.Button(
            "Generate Graphs",
            color="primary",
            block=True,
            id="button",
            className="mb-3",
        ),
        dbc.Tabs(
            [
                dbc.Tab(label="Line Graphs", tab_id="line"),
                dbc.Tab(label="Bar Graph", tab_id="bar"),
                dbc.Tab(label="Filter Table", tab_id="table")
            ],
            id="tabs",
            active_tab="line",
        ),
        html.Div(id="tab-content", className="p-4"),
    ]
)

checklist = dbc.FormGroup(
    [
        dbc.Label("Choose a bunch"),
        dbc.Checklist(
            options=[{"label": hashtag, "value": hashtag} 
                 for hashtag in hashtags],
            value=[],
            id="checklist-input",
        ),
    ]
)

inputs = html.Div(
    [
        dbc.Form([checklist]),
        html.P(id="checklist-output"),
    ]
)

@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab"), Input("store", "data")]
)
def render_tab_content(active_tab, data):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    if active_tab and data is not None:
        if active_tab == "bar":
            return dcc.Graph(figure=data["tags_by_friendcount_fig"])
        elif active_tab == "line":
            return dbc.Row(
                [
                    dbc.Col(dcc.Graph(figure=data["count_tags_fig"]), width=6),
                    dbc.Col(dcc.Graph(figure=data["users_per_hour_fig"]), width=6),
                ]
            )
        if active_tab == "table":
            table = dbc.Table.from_dataframe(table_of_interest, striped=True, bordered=True, hover=True)
            return table
    return "No tab selected"

@app.callback(
    Output("checklist-output", "children"),
    [Input("checklist-input", "value")]
)
def multi_tag_analysis(checklist_value):
# How many tweets contained the tags in checklist_value
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

    # Checking if hashtag was used in text and creating a dataframe containing tag,user,hour of tweet, and friend count
    tags = list()
    user = list()
    friend_count = list()
    for index,tweet in ja_tweets.iterrows():
      tag_list = list()
      for hashtag in hashtags:
        if hashtag in tweet['text'].lower():
          tag_list.append(hashtag)
      user.append(tweet['user_screenname'])
      friend_count.append(tweet['user_friends_count'])
      tags.append(tag_list)

    multi_tagged_tweets_df = {'tags':tags,'user':user,'friend_count':friend_count}
    multi_tagged_tweets_df = pd.DataFrame(multi_tagged_tweets_df)
    
    # Loop through the rows and check to see if the user checked tags 
    # Are assigned to the tweet. If they are then safe the row
    # and add to a new dataframe.
    save_index=list()
    for index,tweet in multi_tagged_tweets_df.iterrows():
      # check if list1 contains all elements in list2
      result =  all(elem in tweet['tags'] for elem in checklist_value)
      if result:
        save_index.add(index)
    filtered_tweets = multi_tagged_tweets_df.ix[save_index]
    table_of_interest = dbc.Table.from_dataframe(filtered_tweets, striped=True, bordered=True, hover=True)

    max_rows=len(table_of_interest)
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in table_of_interest.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(table_of_interest.iloc[i][col]) for col in table_of_interest.columns
            ]) for i in range(min(len(table_of_interest), max_rows))
        ])
    ])
  
@app.callback(Output("store", "data"), [Input("button", "n_clicks")])
def generate_graphs(n):
    """
    This callback generates three simple graphs from random data.
    """
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

    if not n:
        # generate empty graphs when app loads
        return {k: go.Figure(data=[]) for k in ["tags_by_friendcount_fig", "count_tags_fig", "users_per_hour_fig"]}
    
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


    # save figures in a dictionary for sending to the dcc.Store
    return {"tags_by_friendcount_fig": tags_by_friendcount_fig, "count_tags_fig": count_tags_fig, "users_per_hour_fig": users_per_hour_fig}


if __name__ == '__main__':
    app.run_server(debug=True)

    



