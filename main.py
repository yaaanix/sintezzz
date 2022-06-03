import telebot
from telebot import types
import requests
from collections import defaultdict
from flask import Flask, request



bot = telebot.TeleBot('5300865628:AAEVwVk5b1lwzwTGUAktk008eQG-tfHkFzc')
server = Flask(__name__)
HEROKU_APPNAME = 'sintezzz'


memory = defaultdict(dict)
OUTPUT = "audio.ogg"
def synthesize(text1, speed1, gender1):
    print("Мы начали создавать файл с текстом", text1)
    token = "t1.9euelZqQnZiOls-NjYyYzZuWns7Hze3rnpWanI7IxpvNzJ6NnZyXlMeZyJPl9PcifxVr-e9Vf1u_3fT3Yi0Ta_nvVX9bvw.uoX1gR-jBV7uN8-eQO6TBzeVmQgTyDqFsTRJemCZuI4dzqV6V7_s0lHqzJqJ7hAPEv6o9Z44D-uBg9lxPj6-Dw"
    folder_id = "b1gap88d08l35fj9vh1u"
    url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
    headers = {
        'Authorization': 'Bearer ' + token,
    }

    data = {
        'text': text1,
        'lang': 'ru-RU',
        'voice': gender1,
        'folderId': folder_id,
        'speed': speed1,
         'emotion': 'good',
    }

    with requests.post(url, headers=headers, data=data, stream=True) as resp:
        if resp.status_code != 200:
            raise RuntimeError("Invalid response received: code: %d, message: %s" % (resp.status_code, resp.text))

        for chunk in resp.iter_content(chunk_size=None):
            yield chunk


    print("Мы закончили создавать файл с текстом", text1, "Это файл", OUTPUT)

bot = telebot.TeleBot('5300865628:AAEVwVk5b1lwzwTGUAktk008eQG-tfHkFzc')
# Функция, обрабатывающая команду /start
@bot.message_handler(commands = ["start"])
def start(message):
# пишем стандартную клавиатуру
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('Да')
    item2 = types.KeyboardButton('Нет')
    markup.add(item1, item2) # прикрепляем к клавиатуре две кнопки
    bot.send_message(message.chat.id, 'Привет! Хочешь послушать сказку?', reply_markup = markup) # прикрепляем клавиатуру к сообщению
#функция, отслеживающая нажатие кнопок (оброботчик событий)
@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private': #личное сообщение
        if message.text == 'Да':
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item3 = types.KeyboardButton('Свою')
            item4 = types.KeyboardButton('Из библиотеки')
            markup.add(item3,item4)
            bot.send_message(message.chat.id, 'Хочешь загрузить свою сказку или послушать из библиотеки?', reply_markup = markup)
        elif message.text == 'Свою':
            #bot.send_message(message.chat.id, 'Пришлите мне текст сказки')
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item5 = types.KeyboardButton('Нажми, когда отправишь текст сказки')
            markup.add(item5)
            msg = bot.send_message(message.chat.id, "Напиши мне текст сказки", reply_markup=markup)
            def send(message):
                abby = message.text
                memory[message.chat.id]['Текст'] = abby
            bot.register_next_step_handler(msg, send)
            #print("Я запомнил твой текст")
        # далее - список кнопок со сказками и их аудиофайлами. Пока пишу их просто номерами (1,2,3...,10)
        elif message.text == 'Из библиотеки':
        # прописываем библиотеку сказок
            #bot.send_message(message.chat.id, 'Выберите сказку из списка')
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item6 = types.KeyboardButton('Колобок')
            item7 = types.KeyboardButton('Теремок')
            item8 = types.KeyboardButton('Айболит')
            item9 = types.KeyboardButton('Вредная кошка')
            item10 = types.KeyboardButton('Красная шапочка')
            item11 = types.KeyboardButton('Лиса и заяц')
            item12 = types.KeyboardButton('Мойдодыр')
            item13 = types.KeyboardButton('Гуси-лебеди')
            item14 = types.KeyboardButton('Под грибом')
            item15 = types.KeyboardButton('Принцесса на горошине')
            markup.add(item6, item7, item8, item9, item10, item11, item12, item13, item14, item15)
            bot.send_message(message.chat.id, 'Выбери сказку из списка', reply_markup = markup)
        # скорость
        elif message.text in ['Нажми, когда отправишь текст сказки']:
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item16 = types.KeyboardButton('Маленькая скорость')
            item17 = types.KeyboardButton('Средняя скорость')
            item18 = types.KeyboardButton('Большая скорость')
            markup.add(item16,item17, item18)
            bot.send_message(message.chat.id, 'Выбери скорость, с которой хочешь прослушать сказку',  reply_markup = markup)

        elif message.text in ['Колобок', 'Теремок', 'Айболит', 'Вредная кошка', 'Красная шапочка', 'Лиса и заяц', 'Мойдодыр', 'Гуси-лебеди', 'Под грибом', 'Принцесса на горошине']:
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item16 = types.KeyboardButton('Маленькая скорость')
            item17 = types.KeyboardButton('Средняя скорость')
            item18 = types.KeyboardButton('Большая скорость')
            markup.add(item16,item17, item18)
            text_to_spell = open(message.text + ".txt").read()
            memory[message.chat.id]['Текст'] = text_to_spell
            bot.send_message(message.chat.id, 'Выбери скорость, с которой хочешь прослушать сказку',  reply_markup = markup)
        # голос
        elif message.text in ['Маленькая скорость', 'Средняя скорость', 'Большая скорость']:
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item19 = types.KeyboardButton('Женский голос')
            item20 = types.KeyboardButton('Мужской голос')
            dictionary = {'Маленькая скорость': '0.8', 'Средняя скорость': '1.0', 'Большая скорость': '1.2'}
            message.text = dictionary[message.text]
            memory[message.chat.id]['speed'] = message.text

            markup.add(item19,item20)
            bot.send_message(message.chat.id, 'Выбери голос, который будет читать сказку', reply_markup= markup )
        # файл + прописать прогу, которая будет кидать файл
        elif message.text in ['Мужской голос', 'Женский голос']:
            dictionary1 = {'Мужской голос': 'filipp', 'Женский голос': 'alena'}
            message.text = dictionary1[message.text]
            memory[message.chat.id]['gender'] = message.text
            desired_speed = memory[message.chat.id]['speed']
            desired_tale = memory[message.chat.id]['Текст']
            desired_gender = memory[message.chat.id]['gender']
            #print("Сейчас будем вызывать синтез")
            #synthesize(desired_tale)
            with open(OUTPUT, "wb") as f:
                for audio_content in synthesize(desired_tale, desired_speed, desired_gender):
                    f.write(audio_content)
            #print("Мы вызвали синтез")
            bot.send_audio(message.chat.id, open(OUTPUT, "rb"))
            bot.send_message(message.chat.id, 'Лови файл! Если захочешь прослушать еще одну сказку, напиши команду /start', reply_markup=types.ReplyKeyboardRemove()) #убираем клавиатуру
# часть, где человек вначале отвечает, что не хочет слушать сказку
        elif message.text == 'Нет':
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item21 = types.KeyboardButton('Да, я не хочу слушать ваши сказки')
            item22 = types.KeyboardButton('Я передумал(а). Хочу послушать сказку!')
            markup.add(item21, item22)
            bot.send_message(message.chat.id, 'Точно?',  reply_markup = markup)
        # возвращение назад (цикл2)
        elif message.text == 'Я передумал(а). Хочу послушать сказку!':
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item3 = types.KeyboardButton('Свою')
            item4 = types.KeyboardButton('Из библиотеки')
            markup.add(item3,item4)
            bot.send_message(message.chat.id, 'Хочешь загрузить свою сказку или послушать из библиотеки?', reply_markup = markup)
        elif message.text == 'Да, я не хочу слушать ваши сказки':
            bot.send_message(message.chat.id, 'Прощай и ничего не обещай. И ничего не говори. А чтоб понять мою печаль, в пустое небо посмотри!', reply_markup=types.ReplyKeyboardRemove())
try: 
    bot.polling(none_stop=True)
except Exception:
    pass


@server.route(f"/{bot}", methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
	bot.remove_webhook()
	bot.set_webhook(url=f"https://sintezzz.herokuapp.com/{bot}") 
	return "?", 200
print('Здарова')
server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

