import telebot
import webbrowser
from telebot import types
import sqlite3
import requests
import json
from currency_converter import CurrencyConverter



bot = telebot.TeleBot("6429172764:AAEQCVn2hGu7fh5wtZffIGWngAJsmeBTAVg")
name = None

@bot.message_handler(commands=["site","website"])
def site(message):
    webbrowser.open("https://test-site-good.tilda.ws/page12345ru")

@bot.message_handler()
def main(message):
    if message.text.lower() == "привет":
        bot.send_message(message.chat.id, f"Привет,{message.from_user.first_name} я бот, который поможет тебе с регистрацией!")
        bot.register_next_step_handler(message,information)
        
@bot.message_handler(commands=['information'])
def information(message):
    bot.send_message(message.chat.id, 'Список команд:  Привет(краткая информация о боте),\n site(открытие сайта),\nhelp(технические менеджеры)\nlogin(регистрация пользователя)')



@bot.message_handler(commands=['help'])
def get_site(message):
    bt = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text='Переход на сайт', url= 'https://test-site-good.tilda.ws/page12345ru')
    btn3 = types.InlineKeyboardButton(text='Технический менеджер (Артем)', url='https://vk.com/id522748848')
    btn2 = types.InlineKeyboardButton(text='Технический менеджер (Владимир)', url='https://vk.com/vladimir.logunov')
    bt.add(btn1 ,btn2, btn3)
    bot.send_message(message.chat.id, "По всем проблемам обращаться к  нашим крутым менеджерам", reply_markup=bt)



@bot.message_handler(commands=['login'])
def start(message):
    conn = sqlite3.connect('my_bd.sql')
    cur = conn.cursor()

    cur.execute(
        'CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50))')
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Привет сейчас тебя зарегистрируем! Введите ваше имя :  ')
    bot.register_next_step_handler(message, user_name)


def user_name(message):
    global name
    name = message.text.strip()

    bot.send_message(message.chat.id, ' Введите пароль:  ')
    bot.register_next_step_handler(message, user_pass)


def user_pass(message):
    password = message.text.strip()

    conn = sqlite3.connect('my_bd.sql')
    cur = conn.cursor()

    cur.execute(f"INSERT INTO users (name, pass) VALUES ('%s', '%s')"% (name, password))
    conn.commit()
    cur.close()
    conn.close()

    markup = types.InlineKeyboardMarkup()
    bot.send_message(message.chat.id, ' Пользователь зарегистрирован!', reply_markup=markup)
    # bot.register_next_step_handler(message, user_pass)
@bot.callback_query_handler(func= lambda call: True)
def callback(call):
    conn = sqlite3.connect('my_bd.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM users')
    users = cur.fetchall()

    info = ''
    for el in users:
        info += f'Имя: {el[1]}, пароль: {el[2]}\n'

    cur.close()
    conn.close()

    bot.send_message(call.message.chat.id, info)

bot.polling(none_stop=True)




