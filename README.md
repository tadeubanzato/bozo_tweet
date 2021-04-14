# Robô Tweet to Telegram
Robô em Python que faz o scraping do Twitter e posta os últimos posts dos usuários em um grupo do Telegram. Este robô também funciona para enviar os Tweets para uma conta individual ou um canal no Telegram.

## Autenticação do Twitter
Para começar você tem que pedir acesso a API do twitter para conectar o seu programa na plataforma e buscar os dados do usuário desejado.
Para solicitar o acesso a API do Twitter entre no link
https://developer.twitter.com/en

## API do Telegram
Você também tem que conseguir uma API para o Telegram e é muito mais simples fazer isso basta:
1. Entrar no Telegram
2. Abrir o robô do Telegram chamado **BotFather**
3. Seguir com os comandos abaixo
**/newbot** -> Solicitar novo robô
**/token** -> Para o novo token da API
**/setname** -> Para definir um nome ao Robo
**/setuserpic** -> Para adicionar uma foto
**/setprivacy** -> Caso queira usar o robo em um grupo ou canal


### Imports em Python
```python
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
```
Para instalar os requirements use:
`pip install -r requirements.txt

`
### Configurar a API do Twitter
Após o seu acesso a API do twitter ser garantido atualize o código com os dados:
```python
auth = tweepy.OAuthHandler("CONSUMER_KEY", "CONSUMER_SECRET")
auth.set_access_token("ACCESS_TOKEN","ACCESS_TOKEN_SECRET")
```

### Configurando API do Telegram
```python
telegram_token = 'TELEGRAM API TOKEN'
chat_id = 'CHAT ID' # Channel ID
bot = telegram.Bot(token=telegram_token)
```

### Configurar os usuário do Twitter
```python
if __name__ == "__main__":
    # Deinir os usuários do twitter que vc quer verificar
    main(['twitter01','twitter02','twitter03']
```
Usar o handler do twitter dos usuários

### Ler e Escrever CSV
Abaixo o código que vai verificar se o tweet já foi salvo ou não.
É preciso que o CSV já esteja no diretório porque tive preguiça de fazer a validação se o arquivo já existe ou não.
```python
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

```
