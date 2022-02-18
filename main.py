import random
import telebot
from telebot import types
import requests
import json

QIWI_TOKEN = '8b9f0f50831a5766ddf99e5cd3345fdc'
QIWI_ACCOUNT = 'SEESONRISE'
PRICE = 0
bot = telebot.TeleBot('5012064364:AAGzSuit3OgnnNqmYcbhaUujYYx323Ho4LM')
print("Запуск")
oplata = False
oned = ['cUJBmDT7SHEz5Zk0', 'bsK6TDWn95vqw2MJ', '3CWI6FMSBluhRf28', 'k7mQF246ZxjgBzse', 'sBmuwXySaNOgl7ZD',
        'oI5WAqLFQ1CNtPfO', '32kAfx5mXPnTJyWl', 'OCSuWQwytLzMgRIY', 'jBY2Jvnx7Htg3LwG', '1Xjehsl48gU5arfq']
choiseone = random.choice(oned)
sevend = ['svFBejUghQV3qWmw', 'w7YkfUqQnODa9TrJ', '3bpAaoWV94gxBCsM', 'jCK5hgM4TWwDIU1O', 'vz01YdIDxemUB7Nq',
          'WqZ6JSwoPXQbN7au', 'rse0mK3BQkwuEV1X', '7e42mNPirGElgLDA', '5u7IQXG8a1fckYdn']
choiseseven = random.choice(sevend)
mouth = ['QT8sRd3FfZGIpOo4', 'Xh6RWY5Lzgv1foS3', 'NWZ3Gd4RpVCtIzxj', 'L3JAHnZgTxPG7zCD', '7KmwME8k2o09ZFyl',
         'I8P0ORTCD2UjYuch', 'hp4zyaJ1DfwKXtTc', 'HVRLQAxKUEn6pCga', 'tezIin9ADb5QHWvS', 'htqWFO5K3Nnmiy78']
choisemouth = random.choice(mouth)
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.from_user.id, "Привет\nЭто бот создан для продажи програмы для генерации сид фраз")
    keybord = types.ReplyKeyboardMarkup()
    key_one = types.KeyboardButton(text='Купить')
    key_two = types.KeyboardButton(text='Помощь')
    keybord.add(key_two, key_one)
    bot.send_message(message.from_user.id, "Если заинтересовался пиши /buy или жмякай на кнопку", reply_markup=keybord)


@bot.message_handler(content_types=['text'])
def get_text(message):
    global oplata
    if message.text == 'Купить':
        bot.send_message(message.from_user.id, "Вот весь товар, он возможно будет увеличиваться",
                         reply_markup=types.ReplyKeyboardRemove())
        keybord = types.InlineKeyboardMarkup()
        buy1 = types.InlineKeyboardButton(text='Купить програму на день ', callback_data='1')
        buy2 = types.InlineKeyboardButton(text='Купить програму на неделю ', callback_data='2')
        buy3 = types.InlineKeyboardButton(text='Купить програму на месяц ', callback_data='3')
        keybord.add(buy1, buy2, buy3)
        bot.send_message(message.from_user.id, "Ну выбирай товар", reply_markup=keybord)
    elif message.text == "Оплатить":

        if oplata == True:

            global random_code
            random_code = random.randint(100000, 999999)
            keyboard = types.InlineKeyboardMarkup()
            callback_button = types.InlineKeyboardButton(text="Проверить", callback_data="start")
            keyboard.add(callback_button)
            bot.send_message(message.chat.id, f'Счет\n\nПополнение счета на сумму: {PRICE}RUB.'
                                              f'\nСтатус: Не оплачено\n\nОплатите счет QIWI:qiwi.com/n/{QIWI_ACCOUNT}.'
                                              f'\nВ комментарий к оплате оставьте: {random_code}.',
                             reply_markup=keyboard)
        else:
            bot.send_message(message.from_user.id, "У вас нет заказов")
    elif message.text == "Отмена":
        if oplata == True:
            keybord = types.ReplyKeyboardMarkup()
            key_one = types.KeyboardButton(text='Купить')
            key_two = types.KeyboardButton(text='Помощь')
            keybord.add(key_two, key_one)
            oplata = False
            bot.send_message(message.from_user.id, 'Ваш заказ отменён', reply_markup=keybord)
        elif oplata == False:
            keybord = types.ReplyKeyboardMarkup()
            key_one = types.KeyboardButton(text='Купить')
            key_two = types.KeyboardButton(text='Помощь')
            keybord.add(key_two, key_one)
            bot.send_message(message.from_user.id, 'У вас нет активных заказов', reply_markup=keybord)
    elif message.text == "Помощь":
        bot.send_message(message.from_user.id, "Вот ссылка на гайд по програме")
    elif message.text == '/help':
        bot.send_message(message.from_user.id, "Вот ссылка на гайд по програме")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global PRICE
    if call.data == '1':
        keybord = types.ReplyKeyboardMarkup()
        accept = types.KeyboardButton(text='Оплатить')
        keybord.add(accept)
        cancel = types.KeyboardButton(text='Отмена')
        keybord.add(cancel)
        answer = 'Ваш товар "Ключ на один день" если всё верно нажмите на кнопку оплатить'
        bot.send_message(call.message.chat.id, answer, reply_markup=keybord)
        PRICE = 500
        print("anal")
        global oplata
        oplata = True
    elif call.data == "start":
        h = requests.get('https://edge.qiwi.com/payment-history/v1/persons/' + QIWI_ACCOUNT + '/payments?rows=50',
                         headers={'Accept': 'application/json',
                                  'Content-Type': 'application/json',
                                  'Authorization': f'Bearer {QIWI_TOKEN}'})
        req = json.loads(h.text)
        for i in range(len(req['data'])):
            if req['data'][i]['comment'] == f"{random_code}":
                if req['data'][i]['sum']['amount'] == PRICE:
                    bot.send_message(call.message.chat.id, 'Вас заскамили)')
                    if PRICE == 100:
                        bot.send_message(call.message.chat.id, f'Вот ваша ключ {choiseone}')
                    elif PRICE == 1000:
                        bot.send_message(call.message.chat.id, f'Вот ваша ключ {choiseseven}')
                    elif PRICE == 5000:
                        bot.send_message(call.message.chat.id, f'Вот ваша ключ {choisemouth}')
    elif call.data == '2':
        keybord = types.ReplyKeyboardMarkup()
        accept = types.KeyboardButton(text='Оплатить')
        keybord.add(accept)
        cancel = types.KeyboardButton(text='Отмена')
        keybord.add(cancel)
        answer = 'Ваш товар "Ключ на один неделю" если всё верно нажмите на кнопку оплатить'
        bot.send_message(call.message.chat.id, answer, reply_markup=keybord)
        PRICE = 2000
        print("anal")
        global oplata
        oplata = True
    elif call.data == '3':
        keybord = types.ReplyKeyboardMarkup()
        accept = types.KeyboardButton(text='Оплатить')
        keybord.add(accept)
        cancel = types.KeyboardButton(text='Отмена')
        keybord.add(cancel)
        answer = 'Ваш товар "Ключ на один месяц" если всё верно нажмите на кнопку оплатить'
        bot.send_message(call.message.chat.id, answer, reply_markup=keybord)
        PRICE = 5000
        print("anal")
        global oplata
        oplata = True


bot.polling(none_stop=True, interval=0)
