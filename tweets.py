import logging
import requests
import urllib.request
import json
import tweepy
# import telegram_send
import time
import pandas as pd
from pandas import DataFrame
from telegram import *
from telegram.ext import *
import telegram
from datetime import datetime, timedelta
from heapq import nlargest

# Authenticate to Twitter
auth = tweepy.OAuthHandler("fqEJTntllMFjsBMKgRz0P8IVG", "AIvitbiAl8IFHWjzDWmimfAoVwu94hbB2OC7pFQPbm8BIIqvv6")
auth.set_access_token("1349545148158455812-qReIle2zXNUZRE44jsYQyQbRJQjT78","cDQ2QNrDEQAQdF0laWB0FaDOKDQSB6smWBnrJsESfYNjp")

# Authenticate to Telegram
telegram_token = '1793615020:AAETkLnHht_rTf2Q4db0E3GAvz1GTBag-78'
chat_id = '-1001488988830' # Channel ID
bot = telegram.Bot(token=telegram_token)

def on_status(keywords,api):
    # odiosos = keywords
    for odio in keywords:
        tweet = api.user_timeline(id=odio,count=0)[0]
        name = tweet.user.name
        ##### 10 seconds CountDown timer for next user in the list
        t=(10 * 1)
        while t:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print(f"Validando último tweet de {name}: {timer}                         ", end="\r")
            time.sleep(1)
            t -= 1

        user = tweet.user.screen_name
        teweetid = tweet.id
        message = f'https://twitter.com/{user}/status/{str(teweetid)}'
        # teste = 'https://api.telegram.org/bot1793615020:AAETkLnHht_rTf2Q4db0E3GAvz1GTBag-78/sendMessage?chat_id=-1001488988830&text=test'
        image = tweet.user.profile_image_url
        image = image.replace("normal","400x400")
        source = tweet.source
        source = source.replace('for','para')
        followers = '{:,}'.format(tweet.user.followers_count)
        date = tweet.created_at
        likes = myFloat = '{:,}'.format(tweet.favorite_count)
        retweets = '{:,}'.format(tweet.retweet_count)

        ##### Add icons to specific names
        if 'jair' in name.lower():
            name = f'{name} 💩'
        if 'eduardo' in name.lower():
            name = f'{name} 🍌'

        ##### Open CSV File to verify if Tweet was already posted based on TweetID
        dfopen = pd.read_csv('gabinete_do_mal.csv', index_col=0)
        if not dfopen['tweetid'].eq(teweetid).any():
            bot.send_photo(chat_id, image)
            bot.sendMessage(chat_id=chat_id, text=f"Último tweet por {name} enviado pelo 📱 {source} (da presidência)\n\n🐄 Followers: {followers}\n🐂 Data: {date}\n🥛 Likes: {likes}\n🐮 Retweets: {retweets}\n\nhttps://twitter.com/{tweet.user.screen_name}/status/{str(tweet.id)}")
            # telegram_send.send(images=[image.replace('normal','200x200')])
            # telegram_send.send(messages=[f'Último tweet por {name} enviado pelo 📱 {source} (da presidência)\n\n🐄 Followers: {followers}\n🔥 Data: {date}\n🐮 Likes: {likes}\n🐂 Retweets: {retweets}\n\nhttps://twitter.com/{tweet.user.screen_name}/status/{str(tweet.id)}'])
            dictposts = {'username':[f'@{user}'], 'tweetid':[teweetid], 'name':[name], 'date':[date], 'likes':[likes],'retweets':[retweets],'plinks':[message]}

            ##### Build DataFrame with Pandas and Store on CSV
            df = pd.DataFrame(dictposts)
            df.to_csv('gabinete_do_mal.csv', mode='a', index = False, header = False)
        else:
            print('not added', end="\r")

    ##### 30 minutes CountDown timer for next user in the list
    t=(60 * 30)
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(f"Varredura reiniciará em: {timer}                                        ", end="\r")
        time.sleep(1)
        t -= 1
    return main(keywords)

def main(keywords):
    try:
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        on_status(keywords,api)
    except tweepy.TweepError:
        t=(60 * 20)
        while t:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print(f"Varredura reiniciará em: {timer}                                           ", end="\r")
            time.sleep(1)
            t -= 1
if __name__ == "__main__":
    main(['jairbolsonaro','CarlosBolsonaro','FlavioBolsonaro','BolsonaroSP','CarlaZambelli38','Biakicis','gen_heleno','AbrahamWeint','DamaresAlves','depheliolopes','opropriolavo','GeneralMourao','rsallesmma','fabiofaria'])
