#!/usr/bin/env python3

################################ imports #######################################

import tweepy
from tweepy import OAuthHandler
from nltk.tokenize import word_tokenize
import string
from nltk.corpus import stopwords
import pandas
import subprocess
import shlex
import time
import re
import mysql.connector
from mysql.connector import errorcode
from tweepy.streaming import StreamListener
from tweepy import Stream
import json
import sys

########################### build environment ##################################

# mysql conntection

cnx=mysql.connector.connect(user='###',password='###',host='localhost',database='stock')
cursor = cnx.cursor()
cnx.database ='stock'

# setting up twitter engine

consumer_key = 'mfUJrSOK1zUE0Kpmd5JPRr8FD'
consumer_secret = 'CVs2VgyJpq0oZYSsb1vx6Q5pxVHW5Dd0IT5UenBKYjBMsUHaYY'
access_token = '983672173964550145-wZif1QVpL7vBocnMZdEzs7YCnYfThIe'
access_secret = 'RXT3fhcGtsaDYnmTTWHaT1COtsWpAY3bi0J99s6NtnSxo'

# global temp variable for discorverd brand
global_tmp = ''

# person who is searched for in stream, e.g. @realdonaldtrump
# must be a string argument when starting the script
person=sys.argv[1]  

################################ define functions ##############################

# tokenize string
# unused

def tokenize(phrase):
  
  tokens = word_tokenize(phrase)
  tokens = [w.lower() for w in tokens]
  table = str.maketrans('','',string.punctuation)
  stripped = [w.translate(table) for w in tokens]
  words = [word for word in stripped if word.isalpha()]
  stop_words = set(stopwords.words('english'))
  stop_words.add('inc')
  stop_words.add('corp')
  words = [w for w in words if not w in stop_words] 
 
  return words 

# search for twitter company accounts, e.g. @Apple, gets data from brand table of stock database
# tweet as untokenized string
def search_for_twitter_comp(tweet) : 
  global global_tmp
  return_value = False
  cursor.execute("""SELECT twitter_brand, brandshort FROM brand;""")
  for row in cursor.fetchall() :
    if row[0] != None :
      if row[0] in tweet :
        return_value = True
        global_tmp = row[1]
  return return_value
              
# search for stock_symbols, e.g. $AAPL, retruns True if something was found
# tweet as untokenized string
def search_for_stock(tweet) :
  global global_tmp
  return_value = False
  cursor.execute("""SELECT brandshort from brand;""")
  for row in cursor.fetchall() :
    searchterm = '\$' + row[0]
    if re.findall(r''+searchterm+'\\b', tweet) :
      global_tmp = row[0]
      return_value = True
  return return_value

# insert tweet into tweets table of mysql database for analyse purposes
def insert_tweets_to_mysql(tweet_timestamp, tweet_text, person) :
  global global_tmp
  format_str = """SELECT person_id FROM people WHERE twitter_tag = '{person_id}';"""
  sql_command = format_str.format(person_id = person)
  cursor.execute(sql_command)
  result = cursor.fetchall()
  print(result)
  for row in result :
    person_fk = row[0]
  insert = "INSERT INTO tweets (tweet_text, tweet_timestamp, fk_person, fk_brand) values (%s, %s, %s, %s)".format()
  cursor.execute(insert, (tweet_text, tweet_timestamp, person_fk, global_tmp))
  cnx.commit()

# create class for stream listener
# if text in tweet, search for mentioned companies and if found, start stock data collecting and wite
# tweet into database

class listener(StreamListener):

  def on_data(self, data) :
    all_data = json.loads(data)
    
    if 'text' in all_data:
      tweet = all_data["text"]
      timestamp = all_data["created_at"]
      username = all_data["user"]["screen_name"]
    
      print((username,tweet))
      if search_for_twitter_comp(tweet) :
        insert_tweets_to_mysql(timestamp, tweet, person)
        subprocess.call(shlex.split('/home/sperber/scripts/live_stream/startStockDataCollecting.sh ' + global_tmp))
      if search_for_stock(tweet) :
        insert_tweets_to_mysql(timestamp, tweet, person)
        subprocess.call(shlex.split('/home/sperber/scripts/live_stream/startStockDataCollecting.sh ' + global_tmp))
      
      return True
    else:
      return True
# catch every status error and print it 
# usually most catched error is 420 for to many simultaneous connections
  def on_error(self, status) :
    print(status)
  


########### main ###################

while True :
  try :
    #time.sleep(90) # to avoid to connection errors of to rapidly reconnects 
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
 
    twitterStream = Stream(auth, listener(),  wait_on_rate_limit=True)
    twitterStream.userstream(encoding='utf8', _with=person)

  except tweetstream.ConnectionError as e:
    print('conn')
  except tweetstream.AuthenticationError as e:
    print('auth')







