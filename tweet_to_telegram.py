# tweet_to_telegram.py
# -*- coding: utf-8 -*-

import logging
import requests
import urllib.request
import json
import tweepy
import time
import pandas as pd
from pandas import DataFrame
from telegram import *
from telegram.ext import *
import telegram
from datetime import datetime, timedelta
from heapq import nlargest

# Authenticate to Twitter
auth = tweepy.OAuthHandler("CONSUMER_KEY", "CONSUMER_SECRET")
auth.set_access_token("ACCESS_TOKEN","ACCESS_TOKEN_SECRET")

# Authenticate to Telegram
telegram_token = 'TELEGRAM API TOKEN'
chat_id = 'CHAT ID' # Channel ID
bot = telegram.Bot(token=telegram_token)

def on_status(keywords,api):
    # loop para cada um dos usuários definidos na lista
    for odio in keywords:
        tweet = api.user_timeline(id=odio,count=0)[0]
        name = tweet.user.name

        ##### Contagem regressica para o próximo tweet
        t=(10 * 1)
        while t:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print(f"Validando último tweet de {name}: {timer}                         ", end="\r")
            time.sleep(1)
            t -= 1

        user = tweet.user.screen_name # Pega nome do usuário direto da API do Twitter
        teweetid = tweet.id
        message = f'https://twitter.com/{user}/status/{str(teweetid)}' # Monta o link do post do twitter
        image = tweet.user.profile_image_url # Pega o link da imagem do twitter do usuário
        image = image.replace("normal","400x400") # MAnipula a URL da foto para pegar mesma url da foto com mais qualidade
        source = tweet.source # Pega a fonte do post se foi um iPhone ou Android, por exemplo
        source = source.replace('for','para')
        followers = '{:,}'.format(tweet.user.followers_count) # Pega o numero de followers que o usuário tem
        date = tweet.created_at # Pega a data de quando o tweet foi postado
        likes = myFloat = '{:,}'.format(tweet.favorite_count)
        retweets = '{:,}'.format(tweet.retweet_count)

        ##### Abre o CSV File e verifica se o tweet ja foi salvo
        dfopen = pd.read_csv('gabinete_do_mal.csv', index_col=0)
        if not dfopen['tweetid'].eq(teweetid).any():
            bot.send_photo(chat_id, image)
            bot.sendMessage(chat_id=chat_id, text=f"Último tweet por {name} enviado pelo 📱 {source} (da presidência)\n\n🐄 Followers: {followers}\n🐂 Data: {date}\n🥛 Likes: {likes}\n🐮 Retweets: {retweets}\n\nhttps://twitter.com/{tweet.user.screen_name}/status/{str(tweet.id)}")
            dictposts = {'username':[f'@{user}'], 'tweetid':[teweetid], 'name':[name], 'date':[date], 'likes':[likes],'retweets':[retweets],'plinks':[message]}

            ##### Constroi o DataFrame com Pandas e salva no CSV
            df = pd.DataFrame(dictposts)
            df.to_csv('tweets_salvos.csv', mode='a', index = False, header = False)
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
    # Deinir os usuários do twitter que vc quer verificar
    main(['twitter01','twitter02','twitter03'])
