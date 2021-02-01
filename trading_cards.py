# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 21:27:49 2020

@author: PoisonTree
"""

import tweepy
import sys
import pymongo
import json
#user application credentials
consumer_key="dY9bcu2wRukzQbwM5HoQaByS7"
consumer_secret="EsWO5C0E9zUmQ7wj04YIQy12gcV6Qq2aPVwtmMgjusbxsj18hQ"

access_token="22717107-1wbtQn81N7J5Q6jbX1JIpCFxYgaMISN524DrNXme4"
access_token_secret="3Cnlxy4zQS06t3t6UoenMHNcksK4KRUp4I6oOpioJf0AP"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

class CustomStreamListener(tweepy.StreamListener):
    """
    tweepy.StreamListener is a class provided by tweepy used to access the Twitter 
    Streaming API. It allows us to retrieve tweets in real time.
    """
    def __init__(self, api):
        self.api = api
        super(tweepy.StreamListener, self).__init__()
        # Connecting to MongoDB and use the database twitter.
        self.db = pymongo.MongoClient().tcg
        self.count=0
    def on_data(self, tweet):
        '''
        This will be called each time we receive stream data and store the tweets 
        into the respective collection.
        '''
#        languages = {'en':'en_tweet','ja':'ja_tweet'}

#        for language,collection in languages.items():
#          print(language,collection)
        if self.count < 10000:
          tweet = json.loads(tweet)
          if (tweet['lang']=='ja') and ('retweeted_status' not in tweet):
            self.db.ja_tweet.insert_one(tweet)
            self.count +=1
            print('Tweet #',self.count)
        else:
            print("Reached 5 '{}' Tweets".format('ja')) 
    def on_error(self, status_code):
        # This is called when an error occurs
        print(sys.stderr, 'Encountered error with status code:', status_code)
        return True # Don't kill the stream
 
    def on_timeout(self):
        # This is called if there is a timeout
        print(sys.stderr, 'Timeout.....')
        return True # Don't kill the stream

# Create our stream object
sapi = tweepy.streaming.Stream(auth, CustomStreamListener(api))

sapi.filter(track=['#tradingcards','#sportscards','#whodoyoucollect','#cards','#topps','#tcg','#paniniamerica','#basketballcards','#pokemontcg','#yugioh','#pokemoncards','#footballcards','#yugiohcommunity','#rookiecard','#upperdeck','#tradingcardgame','#baseballcards','#magicthegathering','#cardcollector','#mtg','#psagrade','psa10','#hockeycards','#tradingcard','#cardcollection','#mtgcommunity','#wotc','#yugiohcards','#pokemoncommunity','#yugiohtcg','#sportscardsforsalearthockey','#yugiohcollection','#nbacards','#mtgaddicts','#rookiecards','#donruss','#pokemoncollector','#pokeball','#pokemontrainer','#pokedex','#pokemonswordshield','#pokemonxy','#pokemoncollection','#wizardsofthecoast','#pokemoncard','#pokemonletsgo','#ygo','#pokemontradingcardgame','#swordandshield','#mtgcards','#yugiohcard','#pokemonworld','#yugiohcollector','#ocg','#yugiohzexal','#duellinks','#baseset','#darkmagician','#secretrare','#tcgplayer','#boosterbox','#boosterpack','#pokemontcgcommunity','#rebelclash','#therosbeyonddeath']) 
# sapi.filter(track=['#hillaryclinton','#hillary2016','#imwithher','#historymade']) 
# sapi.filter(track=['#feelthebern','#thankyoubernie','#stillsanders','#bernie2016']) 

# In mongo path type:
# mongoexport --db IPDFinal --collection Tweets --type=csv --fields text,created_at,geo,source --out C:\Users\PoisonTree\Documents\IPD351BigDataNoSQL\output.csv
