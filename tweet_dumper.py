#!/usr/bin/python
# encoding: utf-8

import os, sys
import tweepy #https://github.com/tweepy/tweepy
import csv
from tqdm import tqdm
from googletrans import Translator
import MainControl

#Twitter API credentials
consumer_key = "I0PtW9HXNouIsMTNvA1Uu1C5P"
consumer_secret = "WROrsKk0k9gjJBYpQf336IsZES0JrjXJh1v6x3XXXDqWuI0uTT"
access_key = "3382124832-GN0VaIavsTdQUQuI8CU9TI8JkFNB4GI6qH6DBpH"
access_secret = "bPytulI8nlIh3cvC01U4qwukdYuqRHuGJdna5cZDTi6p4"

def get_all_tweets(screen_name, lang, dest):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	#stream = Stream(auth, l)
	#stream.filter(languages=["ar"])
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print ("getting tweets before {}".format(oldest))
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print("... tweets downloaded so far".format(len(alltweets)))
	
	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = []
	trans = Translator()

	print("Connected to Google Translator...")
	cnt = 0
	translated = 0

	with tqdm(total = 100) as pbar:
		for tweet in alltweets:
			url = "http://twitter.com/{}/status/{}".format(screen_name, tweet.id_str)
			url_text = '=HYPERLINK("{}", "Access details here")'.format(url)
			desc = ''
			try:
				desc = trans.translate(tweet.text, dest="%s" % lang).text
				translated = translated + 1
			except:
				desc = "Couldn't translate this tweet."

			if cnt % (len(alltweets)/100) == 0:
				pbar.update(1)

			cnt = cnt + 1

			date = str(tweet.created_at).split(" ")

			outtweets.append([date[0], desc.encode("utf-8"), tweet.text.encode("utf-8"), url_text])

	print("####################################################")
	print("# A total of {} tweets have been downloaded".format(str(cnt)))
	print("####################################################")
	print("# {} tweets successfully translated".format(str(translated)))
	print("# {} tweets were not translated".format(str(cnt - translated)))
	print("####################################################")

	#write the csv	
	with open('{}/{}_tweets.csv'.format(dest, screen_name), 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(["Date","Translated version","Original tweet","Media source link"])
		writer.writerows(outtweets)
