import telebot
from telebot import types
from config import keys, TOKEN
from extensions import APIException, Converter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: telebot.types.Message):
    text = 'Привет.Я конвертер валют!\n\nЧтобы начать работу введите запрос в следующем формате:\n\
<имя валюты, цену которой вы хотите узнать>\n\
<имя валюты, в которой надо узнать цену первой валюты>\n\
<количество первой валюты, если требуется>\n\nПример:\n<Евро Рубль 50> или <Евро Рубль>'
    bot.send_message(message.chat.id, text)
    buttons(message)


@bot.message_handler(commands=['buttons'])
def buttons(message: telebot.types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Cписок доступных валют")
    item2 = types.KeyboardButton("Инструкция")
    markup.add(item1)
    markup.add(item2)
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:\n'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def message_reply(message):
    if message.text == "Cписок доступных валют":
        values(message)

    elif message.text == "Инструкция":
        send_welcome(message)

    else:
        try:
            value = message.text.lower().split(' ')

            if len(value) == 3:
                quote, base, amount = value
            elif len(value) == 2:
                quote, base = value
                amount = '1'
            else:
                raise APIException('Неверное количество параметров.')

            total_base = Converter.get_price(quote, base, amount)
        except APIException as e:
            bot.reply_to(message, f'Ошибка пользователя\n{e}')
            buttons(message)
        except Exception as e:
            bot.reply_to(message, f'Не удалось обработать команду\n{e}')
            buttons(message)
        else:
            text = f'Цена {amount} {quote} в {base} - {total_base}'
            bot.send_message(message.chat.id, text)
            buttons(message)

bot.polling()