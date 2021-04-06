import pyowm
import telebot
from pyowm.utils import config as cfg
from config import TOKEN, keys, API_KEY
from extensions import *




# config = cfg.get_default_config()
# config['language'] = 'ru'


#owm = pyowm.OWM('cb1c67439cafb9efac7ef14821822512')
bot = telebot.TeleBot(TOKEN, parse_mode=None)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    # bot.send_message(message.chat.id, f'Привет! \n\nВведи наименование города/страны, чтобы узнать погоду')
    bot.send_message(message.chat.id, f'Привет! \n\nВведи <имя валюты> <в какую валюту перевести> <количество> \
        \nCписок доступных валют /values')

# @bot.message_handler(commands=['help'])
# def send_welcome(message):
# 	bot.reply_to(message, "Наименование города/страны просписывается на русском или на английском языке. \nБот покажет текущую облачность, погоду и информацию о ветре")

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = f'Доступные валюты:\n'
    text+="\n".join(keys.keys())
    bot.reply_to(message, text)


# @bot.message_handler(content_types=['text', ])
# def send_weather(message):
#     try:
#         mgr = owm.weather_manager()
#         observation = mgr.weather_at_place(message.text)
#         w = observation.weather
#         temp = w.temperature('celsius')["temp"]
#         wind = w.wind()['speed']
#
#         answer = "Сейчас " + w.detailed_status + "\n"
#         answer += "Температура: " + str(temp) + "\n"
#
#
#         if wind < 5:
#             answer += "Слабый ветер \n\n"
#         elif wind < 14:
#             answer += "Есть ветерок \n\n"
#         elif temp < 10 and wind > 14:
#             answer += "Метель :(( \n\n"
#         elif wind < 25:
#             answer += "Сильный ветер \n\n"
#         elif wind <33:
#             answer += "Очень сильный ветер \n\n"
#         elif wind < 100:
#             answer += "Ураган!!! \n\n"
#
#
#         if temp < -10:
#             answer += "Бррр, ужасно холодно"
#         elif temp < 4 and w.detailed_status == 'ясно':
#             answer += "холодновато, но солнышко:3"
#         elif temp < 4:
#             answer += "и так холодно, когда лучше в одеялку и не выходить"
#         elif temp < 10 and w.detailed_status == 'небольшой дождь' or w.detailed_status == 'дождь':
#             answer += "холодновато и мокро - фю"
#         elif temp < 10:
#             answer += "и холодновато"
#         elif temp < 18:
#             answer += " Ох, прохладненько"
#         elif temp < 24:
#             answer += "Тепло, хорошоо! Отличная погода :3 "
#         elif temp <30:
#             answer += "Жара!"
#         elif temp >= 30:
#             answer += "Нереальная жара"
#
#         bot.reply_to(message, answer)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Должно быть 3 параметра')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    # except Exception as e:
    #     bot.reply_to(message, f'Не удалось обработать команду\n{e}')

    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['photo', ])
def say_lmao(message: telebot.types.Message):
    bot.reply_to(message, 'Хорошая, картинка')

bot.polling(none_stop=True)




