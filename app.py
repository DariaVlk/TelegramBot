import telebot
from config import supportedCurrencies, TOKEN
from extensions import ConvertionExeption, ValueConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите комманду боту в следующем формате: \n <название валюты> ' \
           '<в какую валюту перевести> ' \
           '<колличество переводимой валюты> ' \
           '\n Например: доллар рубль 1' \
           '\n Увидеть список всех доступных валют: /values '
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in supportedCurrencies.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertionExeption('Неверное количество параметров.')

        quote, base, amount = values
        total_base = ValueConverter.get_price(quote, base, amount)
    except ConvertionExeption as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}.')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать комманду\n{e}.')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
