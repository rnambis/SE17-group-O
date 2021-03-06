from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from twitter import Twitter
import pickle

import logging
logging.basicConfig()

import newspaper
import nltk

i = 0
twitter = Twitter()


def unpickle_news():
	#Unpickle news file
	file = open('news/news.data', 'r')
	data = pickle.load(file)
	return data


def poster():
	print 'Twitter job started...'
	news_sources = {'Dailymail' 	: 'http://www.dailymail.co.uk/ushome/index.html',
			'BBC'		: 'http://www.bbc.com/news',
			'The Economist'	: 'http://www.economist.com',
			'CNN' 		: 'http://www.cnn.com',
			'The New York Times': 'https://www.nytimes.com',
			'The Atlantic'	: 'https://www.theatlantic.com',
			'The Guardian'	: 'https://www.theguardian.com/us'}

	news_data = unpickle_news()

	for source in news_sources:
		try:
			for data in news_data[source]:
				print data['summary'] + ' ' + data['url']
				twitter.post(data['summary'] + ' ' + data['url'])
		except:
			print 'something went wrong: ' + source

	print 'Twitter job stopped...'



def social_job():
	scheduler = BackgroundScheduler()
	scheduler.add_job(poster, 'interval', minutes = 5)
	scheduler.start()


if __name__ == '__main__':
	social_job()
