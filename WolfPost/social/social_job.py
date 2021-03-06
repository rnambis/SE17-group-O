from apscheduler.schedulers.background import BackgroundScheduler
from twitter import Twitter

import requests
import logging
logging.basicConfig()


i = 0
twitter = Twitter()
api_key = ''


def poster():
    print 'Twitter job started...'
    news_link_dict={'Dailymail' : 'https://newsapi.org/v1/articles?source=daily-mail&sortBy=top&apiKey=' + api_key,
            'BBC':'https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey=' + api_key,
            'The Economist':'https://newsapi.org/v1/articles?source=the-economist&sortBy=top&apiKey=' + api_key,
            'CNN' : 'https://newsapi.org/v1/articles?source=cnn&sortBy=top&apiKey=' + api_key,
            'The New York Times' : 'https://newsapi.org/v1/articles?source=the-new-york-times&sortBy=top&apiKey=' + api_key,
            'Bloomberg' : 'https://newsapi.org/v1/articles?source=bloomberg&sortBy=top&apiKey=' + api_key,
            'The Guardian' : 'https://newsapi.org/v1/articles?source=the-guardian-uk&sortBy=top&apiKey=' + api_key }

    for key in news_link_dict:
        response = requests.get(news_link_dict[key])
        dict_response = response.json()

        #Get top article for new source
        text = dict_response['articles'][0]['description']
        url =  dict_response['articles'][0]['url']
        twitter.post(text + ' ' + url)

        print text + ' ' + url
        print


def social_job():
    scheduler = BackgroundScheduler()
    scheduler.add_job(poster, 'interval', minutes = 30)
    scheduler.start()


if __name__ == '__main__':
    social_job()
