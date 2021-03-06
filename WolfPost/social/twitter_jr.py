from twython import Twython
import json
import sys
import urllib, cStringIO
import os

class Twitter:

	def __init__(self):
    		APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET = self.get_app_keys()
    		self.twy = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)


	def get_app_keys(self):
		# Get app and oauth keys from json file
    		with open('social/Twitter_Keys') as data_file:
			keys = json.load(data_file)
    		return keys['APP_KEY'], keys['APP_SECRET'], keys['OAUTH_TOKEN'], keys['OAUTH_TOKEN_SECRET']


	def splitter(self, text):
  		chunks = ['']
  		words = text.split()
  
  		for w in words:
			current_chunk = len(chunks) - 1
    			if len(chunks[current_chunk] + w) < 122:
      				chunks[current_chunk] += ' ' + w
    			else:
      				chunks.append('')

		chunks = [str(chunks.index(x) + 1) + '/' + str(len(chunks)) + ' ' + x for x in chunks ]
		return chunks


	def update_status(self, text):
		# Handles api call
		# returns dict
		return self.twy.update_status(status=text)


	def update_status_response(self, text, tweet_id):
		# Handles api call for replying to status
		# returns dict
		return self.twy.update_status(status=text, in_reply_to_status_id=tweet_id)


	def post(self, text):
		# Post whatever text
		# if tweet larger than 140 char
		# split into multiple teets
		# post first tweet
		# post next tweets as replys to original
		if len(text) > 140:
			tweets = self.splitter(text)
			tweet_id = self.update_status(tweets[0])['id']
			for text in tweets[1:]:
				self.update_status_response('@WolfpackPost ' + text, tweet_id)

		else:
			self.update_status(text)


# Post text from twitter using arguments from command line input
if len(sys.argv) > 1:
    t = twitter()
    t.post(" ".join(sys.argv[1:]) )
