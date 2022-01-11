import datetime
import psycopg2
import telebot
from telebot import types
from math import ceil

bot = telebot.TeleBot('5024171612:AAG84-gbpN7mRQJbMyfOovX66ZkxEOnyLu0')

conn = psycopg2.connect(database="t_t", user="postgres", password="9094391", host="localhost", port="5432")
cursor = conn.cursor()

day = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Субботу', 'Воскресенье']

if datetime.datetime.now().month > 8:
    d1 = datetime.datetime.strptime("01-09-" + str(datetime.datetime.now().year), "%d-%m-%Y")
else:
    d1 = datetime.datetime.strptime("31-01-" + str(datetime.datetime.now().year), "%d-%m-%Y")
d2 = datetime.datetime.strptime(str(datetime.datetime.date(datetime.datetime.now())), "%Y-%m-%d")
if datetime.datetime.isoweekday(d1) < 5:
    week_n = ceil(((d2 - d1).days + datetime.datetime.weekday(d1)) / 7)
elif datetime.datetime.isoweekday(d1) == 6:
    week_n = ceil(((d2 - d1).days - 2) / 7)
elif datetime.datetime.isoweekday(d1) == 7:
    week_n = ceil(((d2 - d1).days - 1) / 7)


def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Расписание на сегодня')
    btn2 = types.KeyboardButton('Расписание на завтра')
    btn3 = types.KeyboardButton('Расписание')
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    bot.send_message(message.chat.id, "Сейчас идет " + str(week_n) + " неделя, чем помочь?", reply_markup=markup)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEDUq1hmB7iUFjM4IJQoSMfqfR4Jt_OxwACbgUAAj-VzAqGOtldiLy3NSIE')
    menu(message)


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, "Я показываю расписание группы БИН2002!")
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEDUrFhmCBC6oQw_C0J0pADVtzYNBvlKwACRgEAAiI3jgQiieP6A4eLHiIE')


@bot.message_handler(content_types='text')
def reply_message(message):

    def time_table(a, b):
        cursor.execute(
            "select time_table.subject, time_table.start_time, teacher.full_name from time_table join teacher on "
            "teacher.subject = time_table.subject where day = '" + a + "' and (pos = '-' or pos = '" + b + "') "
            "order by time_table.start_time;")
        row = list(cursor.fetchall())
        mess = ''
        for i in row:
            mess += str(i[0]) + ' '
            mess += str(i[1]) + ' - '
            mess += str(i[2]) + '\n'
        bot.send_message(message.chat.id, mess)

    def week_pos(a):
        if week_n % 2 > 0:
            time_table(a, 'в')
        else:
            time_table(a, 'н')

    if message.text == "Расписание на сегодня":
        if datetime.datetime.weekday(datetime.datetime.now()) < 5:
            week_pos(day[datetime.datetime.weekday(datetime.datetime.now())])
        else:
            bot.send_message(message.chat.id,
                             "В " + day[datetime.datetime.weekday(datetime.datetime.now())] + " не учимся!")
            bot.send_sticker(message.chat.id,
                             'CAACAgIAAxkBAAEDUrVhmCHu7coC0T2qWDhIejufAAFyc-UAAj8BAAIiN44ENDnV16oKRgEiBA')
    if message.text == "Расписание на завтра":
        if datetime.datetime.weekday(datetime.datetime.now()) < 4:
            week_pos(day[datetime.datetime.weekday(datetime.datetime.now()) + 1])
        else:
            bot.send_message(message.chat.id,
                             "В " + (day[datetime.datetime.weekday(datetime.datetime.now()) + 1]) + " не учимся!")
            bot.send_sticker(message.chat.id,
                             'CAACAgIAAxkBAAEDUrVhmCHu7coC0T2qWDhIejufAAFyc-UAAj8BAAIiN44ENDnV16oKRgEiBA')
    if message.text == "Расписание":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Понедельник')
        btn2 = types.KeyboardButton('Вторник')
        btn3 = types.KeyboardButton('Среда')
        btn4 = types.KeyboardButton('Четверг')
        btn5 = types.KeyboardButton('Пятница')
        btn6 = types.KeyboardButton('Назад')
        markup.add(btn1)
        markup.add(btn2)
        markup.add(btn3)
        markup.add(btn4)
        markup.add(btn5)
        markup.add(btn6)
        bot.send_message(message.chat.id, "Выберете день недели", reply_markup=markup)
    if message.text == "Понедельник":
        week_pos(day[0])
    if message.text == "Вторник":
        week_pos(day[1])
    if message.text == "Среда":
        week_pos(day[2])
    if message.text == "Четверг":
        week_pos(day[3])
    if message.text == "Пятница":
        week_pos(day[4])
    if message.text == "Назад":
        menu(message)
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEDUrNhmCDfA1kbsHEzMPpeDwE55iTR2wACZgIAAladvQpDYzS_ujiqhCIE')


bot.infinity_polling()