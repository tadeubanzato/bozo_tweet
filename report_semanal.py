import logging
import json
import time
import pandas as pd
from pandas import DataFrame
from telegram import *
from telegram.ext import *
import telegram
from datetime import datetime, timedelta
from heapq import nlargest

# Authenticate to Telegram
telegram_token = '1793615020:AAETkLnHht_rTf2Q4db0E3GAvz1GTBag-78'
chat_id = '-1001488988830' # Channel ID
bot = telegram.Bot(token=telegram_token)

#######----------- WEEKLY REPORT -----------#######
dfopen = pd.read_csv('gabinete_do_mal.csv', index_col=0)
x=0
pastweek=[]
pandas = 0
while (x<7):
    today = datetime.now() - timedelta(days = x)
    past = today.strftime("%Y-%m-%d")
    pastweek.append(past)
    # pandas = f'dfopen["date"].str.contains("{past}") | "{pandas}"'
    x+=1
# pandas = pandas.replace(' | "0"""""""','').replace('"dfopen','dfopen')
df = dfopen[dfopen["date"].str.contains(pastweek[0]) | dfopen["date"].str.contains(pastweek[1]) | dfopen["date"].str.contains(pastweek[2]) | dfopen["date"].str.contains(pastweek[3]) | dfopen["date"].str.contains(pastweek[4]) | dfopen["date"].str.contains(pastweek[5]) | dfopen["date"].str.contains(pastweek[6])]

counts = df["name"].value_counts().to_dict()
top3 = nlargest(3, counts, key = counts.get) # total number of repeated name on the column

dados = {
    "Jair" : {"salario" : 30934.66, "img" : "jair"},
    "Flavio" : {"salario" : 33763.00, "img" : "flavio"},
    "Carlos" : {"salario" : 33763.00, "img" : "carlos"},
    "Eduardo" : {"salario" : 33763.00, "img" : "eduardo"},
    "Carla" : { "salario" : 33763.00, "img" : "carla"},
    "Abraham": { "salario" : 33763.00, "img" : "weintraub"},
    "Damares" : { "salario" : 30934.70, "img" : "damares"},
    "Olavo" : { "salario" : 000000, "img" : "olavo"},
    "Hamilton" : { "salario" : 30934.66, "img" : "mourao"},
    "Salles" : { "salario" : 30934.70, "img" : "sales"},
    "Faria" : { "salario" : 30934.70, "img" : "fabio"},
    "Bolsonaros" : { "salario" : 30934.70, "img" : "fabio"}
}

for (k, v) in dados.items():
    if k in top3[0]:
        name = k

# print(dados[name])
# print(dados[name]['salario'])
# print(dados[name]['img'])

def salminuto(name):
    if 'Bolsonaros' in name:
        salario = dados['Jair']['salario']+dados['Flavio']['salario']+dados['Carlos']['salario']+dados['Eduardo']['salario']
    else:
        salario = (dados[name]['salario'])

    minuterate = (salario/160)/60
    minutosTwitando = (counts[top3[0]]*15)
    dimGasto = round(minuterate * minutosTwitando, 2)
    return dimGasto
    # '{:,}'.format(dimGasto)

### Send Champion Data
bot.sendMessage(chat_id=chat_id, text=f"🎉")
bot.sendMessage(chat_id=chat_id, text=f"E vamos as resultados da seman\nCAMPEÃO de tweets com {counts[top3[0]]} tweets foi 🥁")
bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
time.sleep(2)
bot.sendMessage(chat_id=chat_id, text=f"🥇 {top3[0]}")
time.sleep(2)
bot.send_photo(chat_id=chat_id, photo=open(f"odiosos/{dados[name]['img']}.png", 'rb'))
bot.sendMessage(chat_id=chat_id, text=f"👯‍♂️")
time.sleep(1)

### MORE DATA
bot.sendMessage(chat_id=chat_id, text=f"Top 3 da semana:\n\n🥇 {top3[0]} - {counts[top3[0]]} twts\n🥈 {top3[1]} - {counts[top3[1]]} twts\n🥉 {top3[2]} - {counts[top3[2]]} twts")
bot.sendMessage(chat_id=chat_id, text=f"🎈")
bot.sendMessage(chat_id=chat_id, text=f"Considerando que o salário de {name} é 💵 mais ou menos R${'{:,}'.format(dados[name]['salario'])} e leva mais ou menos uns 15 minutos 🕐 para cada tweet entre abrir o 📱 telefone, ler e postar")
bot.sendMessage(chat_id=chat_id, text=f"{name} gastou 💸 R${salminuto(name)} do dinheiro do contribuinte twitando essa semana")
semana = salminuto('Bolsonaros')
mes = semana*4
ano = mes*12
bot.sendMessage(chat_id=chat_id, text=f"A 👨‍👨‍👦 família Bolsonaro inteira gastou sozinha, APENAS TWITANDO, R${'{:,}'.format(salminuto('Bolsonaros'))}, que daria mais ou menos:\n💸 Por mês = R${'{:,}'.format(mes)}\n\n💸 Por ano = R${'{:,}'.format(ano)}")
bot.sendMessage(chat_id=chat_id, text=f"Parabéns aos envolvidos! - Segue a programação normal")
# print(f"Essa semana só família Bolsonaro gastou sozinha R${'{:,}'.format(salminuto('Bolsonaros'))}, que daria mais ou menos:\nPor mês = R${'{:,}'.format(mes)}\nPor ano = R${'{:,}'.format(ano)}")
