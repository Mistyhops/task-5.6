import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CurrConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_bot(message: telebot.types.Message):
    text = '''Бот предназначен для получения курсов валют.\nДля получения курса введите сообщение в\
 формате:\n<валюта, которую вы продаете> <валюта, которую вы покупаете> <количество валюты>\nнапример,\
 "рубль доллар 1"'''
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['help'])
def help_bot(message: telebot.types.Message):
    text = '''Для получения текущего курса валюты введите сообщение в формате:
<валюта, которую вы продаете> <валюта, которую вы покупаете> <количество валюты>
например, "рубль доллар 1.6"\nСписок доступных команд:\n/help\n/values'''
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values_bot(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in list(keys.keys())[::2]:
        text = '\n'.join((text, key, ))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    try:
        values = message.text.split()

        if len(values) != 3:
            raise ConvertionException('Неверно введены параметры. Введите /help для получения подсказки.')

        quote, base, amount = values

        amount = CurrConverter.amount_type(amount)

        total_base = CurrConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Невозможно обработать команду.\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base * amount}'
        bot.reply_to(message, text)


bot.polling(none_stop=True)
