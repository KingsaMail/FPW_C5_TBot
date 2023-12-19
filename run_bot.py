"""Проект по написанию телеграмбота."""
import telebot

from extensions import *

from bot_token import TOK  #импорт токена бота и словарь с валютой
    

bot = telebot.TeleBot(TOK)  #создание бота


@bot.message_handler(commands=['start', 'help'])
def handler_start_help(message: telebot.types.Message):
    manual = 'Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, manual)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.BotCommand):
    info = 'Доступные валюты: '
    for key in keys.keys():
        info ='\n'.join((info, key))        
    bot.reply_to(message, info)
    
@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        
        if len(values) != 3:
            raise APIException('Слишком много параметров')
        
        quote, base, amount = message.text.split(' ')    #получаем что куда и сколько надо перевести
        price = CryptoConverter.get_price(quote, base, amount)     # получаем сумму
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду {e}')
        
    else:
        text = f'Цена {amount} {quote} в {base} - {price*float(amount)}'
        bot.send_message(message.chat.id, text)
    

bot.polling(none_stop=True)