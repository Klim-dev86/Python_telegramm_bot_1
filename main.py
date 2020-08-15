import requests
from bs4 import BeautifulSoup as BS

import telebot
from telebot import types

bot = telebot.TeleBot('secret_token_:)')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    
    if message.text == "/help":
        bot.send_message(message.from_user.id, "Введи число интересующего тебя дня или нажми что угодно для вызова меню")

    elif message.text in [str(i) for i in range(30)]:
        result = get_weather()
        
        for i in range(len(result)):
            
            if result[i][0].strip() == message.text:
                bot.send_message(message.from_user.id, prepare_message(result[i]))
                continue
    
    else:
         
        keyboard = types.InlineKeyboardMarkup()

        key_today = types.InlineKeyboardButton(text='Сегодня', callback_data='today')

        keyboard.add(key_today)

        key_tomorrow = types.InlineKeyboardButton(text='Завтра', callback_data='tomorrow')

        keyboard.add(key_tomorrow)

        key_day_after_tomorrow = types.InlineKeyboardButton(text='Послезавтра', callback_data='day_after_tomorrow')

        keyboard.add(key_day_after_tomorrow)

        key_next_weekend = types.InlineKeyboardButton(text='Ближайшие выходные', callback_data='next_weekend')

        keyboard.add(key_next_weekend)

        key_in_two_weeks = types.InlineKeyboardButton(text='Через две недели', callback_data='in_two_weeks')

        keyboard.add(key_in_two_weeks)

        key_in_month = types.InlineKeyboardButton(text='Через месяц', callback_data='in_month')

        keyboard.add(key_in_month)
        
        bot.send_message(message.from_user.id, text='Выбери день, для которого ты хочеш узнать прогноз погоды в Ярославле', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)

def callback_worker(call):

    result = get_weather()

    if call.data == 'today':
        msg = prepare_message(result[0])
        bot.send_message(call.message.chat.id, msg)

    if call.data == 'tomorrow':
        msg = prepare_message(result[1])
        bot.send_message(call.message.chat.id, msg)

    if call.data == 'day_after_tomorrow':
        msg = prepare_message(result[2])
        bot.send_message(call.message.chat.id, msg)

    if call.data == 'next_weekend':

        for i in range(len(result)):
            if result[i][2] == "Суббота":
                msg_1 = prepare_message(result[i])
                bot.send_message(call.message.chat.id, msg_1)
                msg_2 = prepare_message(result[i+1])
                bot.send_message(call.message.chat.id, msg_2)
                break
            else:
                continue

    if call.data == 'in_two_weeks':
        msg = prepare_message(result[13])
        bot.send_message(call.message.chat.id, msg)

    if call.data == 'in_month':
        msg = prepare_message(result[30])
        bot.send_message(call.message.chat.id, msg)


def prepare_message(result):
    msg = f'Погода на {result[0]} {result[1]} {result[2]} : \n \
    Температура {result[3]}C,  {result[4]}. \n \
    Скорость ветра - {result[5]}. \n \
    Давление - {result[6]}.'
    
    return msg


def get_weather():

    req = requests.get('https://pogoda33.ru/погода-ярославль/месяц')
    html = BS(req.content, 'html.parser')

    def class_filter(css_class):
        classes = ('day col-md p-2 month-border border-left-0 border-top-0 text-truncate',
                    'day col-md p-2 month-border border-left-0 border-top-0 text-truncate weekend')
        
        return css_class in classes


    lst = html.find_all("div", class_=class_filter)

    result = []
    i = 0

    for el in lst:

        date = el.find_all('span', class_='date')[0].text
        month = el.find_all('span', class_='date d-md-none')[0].text
        day = el.find_all('small', class_='col d-md-none text-right text-muted')[0].text
        temp = el.find_all('span', class_='forecast-temp temp')[0].text.replace(' ', '')
        description = el.find_all('span', class_='precipitation-description')[0].text
        
        try:
            wind = el.find_all('span', class_='wind-count')[0].text
            pressure = el.find_all('span', class_='pressure-count')[0].text 
        except Exception:
            wind = 'неизвестна'
            pressure = 'неизвестно'

        result.append([])
        result[i].append(date)
        result[i].append(month)
        result[i].append(day)
        result[i].append(temp)
        result[i].append(description)
        result[i].append(wind)
        result[i].append(pressure)

        i += 1

    return result


bot.polling(none_stop=True, interval=0)