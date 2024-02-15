import telebot

import os

from fuzzywuzzy import fuzz

bot = telebot.TeleBot('6429172764:AAEQCVn2hGu7fh5wtZffIGWngAJsmeBTAVg')

# Загружаем список фраз и ответов в массив

mas=[]

if os.path.exists('./dialog.txt'):

    f=open('./dialog.txt', 'r', encoding='UTF-8')

    for x in f:

        if(len(x.strip()) > 2):

            mas.append(x.strip().lower())

    f.close()

# С помощью fuzzywuzzy определяем наиболее похожую фразу и выдаем в качестве ответа следующий элемент списка

def answer(text):

    try:

        text=text.lower().strip()

        if os.path.exists('./dialog.txt'):

            a = 0

            n = 0

            nn = 0

            for q in mas:

                if('u: ' in q):

                    # Изучаем, насколько похожи две строки

                    aa=(fuzz.token_sort_ratio(q.replace('u: ',''), text))

                    if(aa > a and aa!= a):

                        a = aa

                        nn = n

                n = n + 1

            s = mas[nn + 1]

            return s

        else:

            return 'Не смог'

    except:

        return 'Ошибка'

# Команда «Старт»

@bot.message_handler(commands=["start"])

def start(m, res=False):

        bot.send_message(m.chat.id, 'Давай поболтаем. Например, напиши мне Привет!')

# Получение сообщений от клиента

@bot.message_handler(content_types=["text"])

def handle_text(message):

    # Запись ответа

    s=answer(message.text)

    # Отправка ответа

    bot.send_message(message.chat.id, s)

# Запускаем бота

bot.polling(none_stop=True, interval=0)