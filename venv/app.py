import telebot # импорт из библиотеки телебот
from config import keys, TOKEN # импортируем из файла config ключи
from utils import ConvertionException, CryptoConverter # импортируем из файла utils классы

bot = telebot.TeleBot(TOKEN) #присваеваем переменной ТOKEN

@bot.message_handler(commands=['start', 'help']) # добавляем метод с командами: старт и помощь
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате: \<название валюты> \
     \<в какую валюту перевести> \ <количество переводимой валюты> ' \
           '\nУвидеть писок  всех доступных валют: /values'
    bot.reply_to(message, text) # бот должен отреагировать на запрос

@bot.message_handler(commands=['values']) # добавляем  метод реакциии на нажатие слова "values" в боте
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ]) # в данном методе прописаны исключения
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertionException('Слишком много параметров.')

        quote, base, amount = values
        new_price = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {new_price}'
        bot.send_message(message.chat.id, text)


bot.polling()