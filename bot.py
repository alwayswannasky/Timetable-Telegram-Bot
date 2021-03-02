from datetime import datetime
import telebot
from telebot import types
import config
import cx_Oracle
import time
import schedule
from multiprocessing.context import Process
import requests

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, config.greeting)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def sent_text(message):
    if message.text.lower() == '/timetable':
        choose_direction(message)
    elif message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'И тебе привет!')
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Еще увидимся!)')
    elif message.text.lower() == 'спасибо':
        bot.send_message(message.chat.id, 'Всегда рад помочь :)')
    elif message.text.lower() == '/time':
        bot.send_message(message.chat.id, config.time)
    elif message.text.lower() == '/groups':
        bot.send_message(message.chat.id, config.groups_data)
    elif message.text.lower() == '/typeofweek':
        bot.send_message(message.chat.id, 'Эта неделя {}.'.format(
            'числитель' if datetime.today().isocalendar()[1] % 2 == 0 else 'знаменатель'))
    elif message.text.lower() == '/weather':
        weather = ''
        bot.send_message(message.chat.id, get_weather(weather))
    # Реализация отправки сообщения по расписанию
    elif message.text.lower() == '/sub':
        subscription(message)
    else:
        bot.send_message(message.chat.id, 'Не понимаю тебя :(')
    log(message)


def choose_direction(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text=config.groups[0], callback_data='Math'))
    keyboard.add(types.InlineKeyboardButton(text=config.groups[1], callback_data='Pmi'))
    keyboard.add(types.InlineKeyboardButton(text=config.groups[2], callback_data='MiMM'))
    keyboard.add(types.InlineKeyboardButton(text=config.groups[3], callback_data='MiKN'))
    keyboard.add(types.InlineKeyboardButton(text=config.groups[4], callback_data='MK'))
    bot.send_message(message.from_user.id, text='Выбери своё направление подготовки:', reply_markup=keyboard)


def choose_direction_by_back(call):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text=config.groups[0], callback_data='Math'))
    keyboard.add(types.InlineKeyboardButton(text=config.groups[1], callback_data='Pmi'))
    keyboard.add(types.InlineKeyboardButton(text=config.groups[2], callback_data='MiMM'))
    keyboard.add(types.InlineKeyboardButton(text=config.groups[3], callback_data='MiKN'))
    keyboard.add(types.InlineKeyboardButton(text=config.groups[4], callback_data='MK'))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Выбери своё направление подготовки:',
                          reply_markup=keyboard)


def course(call):
    stud = Students_dict[0]

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='1', callback_data='1'))
    keyboard.add(types.InlineKeyboardButton(text='2', callback_data='2'))
    keyboard.add(types.InlineKeyboardButton(text='3', callback_data='3'))
    keyboard.add(types.InlineKeyboardButton(text='4', callback_data='4'))
    keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="Back_to_choose"))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Ты выбрал направление подготовки - ' + config.groupsDict[
                              stud.table_group] + ', выбери курс:',
                          reply_markup=keyboard)


def course_magistracy(call):
    stud = Students_dict[0]

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='1', callback_data='1'))
    keyboard.add(types.InlineKeyboardButton(text='2', callback_data='2'))
    keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="Back_to_choose"))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Ты выбрал направление подготовки - ' + config.groupsDict[
                              stud.table_group] + ', выбери курс:',
                          reply_markup=keyboard)


def day(call):
    stud = Students_dict[0]

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Сегодня', callback_data='Today'))
    keyboard.add(types.InlineKeyboardButton(text='Завтра', callback_data='Tomorrow'))
    keyboard.add(types.InlineKeyboardButton(text='Неделя', callback_data='Week'))
    keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="Back_to_course"))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Ты выбрал направление подготовки - ' + config.groupsDict[
                              stud.table_group] + ', курс - ' + stud.table_course,
                          reply_markup=keyboard)


Students_dict = {}


class Student:

    def __init__(self, group):
        self.table_group = group
        self.table_course = None
        self.table_day = None
        self.string = None
        self.tmp = None
        self.number_of_lessen = None
        self.id = None
        self.name = None


def call_course(call):
    stud = Student(call.data)
    Students_dict[0] = stud

    course(call)


def call_course_magistracy(call):
    stud = Student(call.data)
    Students_dict[0] = stud

    course_magistracy(call)


def call_day(call):
    stud = Students_dict[0]
    stud.table_course = call.data

    day(call)


def call_timetable(call):
    stud = Students_dict[0]
    stud.table_day = call.data

    timetable(call)


def timetable(call):
    stud = Students_dict[0]
    stud.string = ' '
    if stud.table_day == 'Today':
        step_one(datetime.today().isoweekday(), 0)
    elif stud.table_day == 'Tomorrow':
        step_one((datetime.today().isoweekday() + 1) % 7, 0)
    elif stud.table_day == 'Week':
        for days in range(7):
            step_one(days + 1, 1)
            bot.send_message(chat_id=call.message.chat.id, text=stud.string)
            stud.string = ' '

        week_for = "Расписание на неделю для: {}, курс - {}".format(config.groupsDict[stud.table_group], stud.table_course)
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="Back_to_day"))
        bot.send_message(chat_id=call.message.chat.id, text=week_for, reply_markup=keyboard)
        return

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="Back_to_day"))

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=stud.string, reply_markup=keyboard)


def step_one(today, is_week):
    stud = Students_dict[0]
    stud.number_of_lessen = 0
    with cx_Oracle.connect(config.orcl_user, config.orcl_password, config.orcl_dns, encoding="UTF-8") as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM couples where день_недели='{}' and специальность='{}' and курс='{}' "
                       "order by ПАРА, ПОДГРУППА".format(config.table[today], config.table[stud.table_group], stud.table_course))

        if is_week != 1:
            stud.string = "{} , курс - {}\n".format(config.groupsDict[stud.table_group], stud.table_course)

        stud.string += "День недели: {}\n".format(config.days_of_week[today])
        for row in cursor:
            if row[8] == 2 and stud.number_of_lessen != row[3]:
                step_two(row)
            elif row[8] == 2 and stud.tmp == 1:
                step_two(row)
            elif row[8] == type_of_week():
                step_two(row)

        if len(stud.string) <= 75:
            stud.string += config.space + '\n' + 'Сегодня нет пар.'

        connection.commit()


def step_two(row):
    stud = Students_dict[0]

    stud.string += config.space + '\n' + 'Пара: ' + str(row[3]) + '\n'

    if row[9] == 3:
        step_three(row)
    if row[9] == 1 or row[9] == 2:
        if row[9] == 1:
            stud.string += '1 подгруппа'
            step_three(row)
            stud.tmp = 1
        if row[9] == 2:
            stud.string += '2 подгруппа'
            step_three(row)
            stud.tmp = 0

    stud.number_of_lessen = row[3]


def step_three(row):
    stud = Students_dict[0]
    stud.string += ' - ' + row[4] + row[5] + ',' + '\n' + row[6] + ', ' + row[7] + '\n'


def type_of_week():
    return datetime.today().isocalendar()[1] % 2


@bot.callback_query_handler(func=lambda call: call.data == 'Back_to_choose')
def call_math(call):
    choose_direction_by_back(call)


@bot.callback_query_handler(func=lambda call: call.data == "Back_to_course")
def call_math(call):
    stud = Students_dict[0]

    if stud.table_group != 'MK':
        course(call)
    else:
        course_magistracy(call)


@bot.callback_query_handler(func=lambda call: call.data == 'Back_to_day')
def call_math(call):
    day(call)


@bot.callback_query_handler(func=lambda call: call.data == "Math")
def call_math(call):
    call_course(call)


@bot.callback_query_handler(func=lambda call: call.data == 'Pmi')
def call_math(call):
    call_course(call)


@bot.callback_query_handler(func=lambda call: call.data == 'MiMM')
def call_math(call):
    call_course(call)


@bot.callback_query_handler(func=lambda call: call.data == 'MiKN')
def call_math(call):
    call_course(call)


@bot.callback_query_handler(func=lambda call: call.data == 'MK')
def call_math(call):
    call_course_magistracy(call)


@bot.callback_query_handler(func=lambda call: call.data == '1')
def call_math(call):
    call_day(call)


@bot.callback_query_handler(func=lambda call: call.data == '2')
def call_math(call):
    call_day(call)


@bot.callback_query_handler(func=lambda call: call.data == '3')
def call_math(call):
    call_day(call)


@bot.callback_query_handler(func=lambda call: call.data == '4')
def call_math(call):
    call_day(call)


@bot.callback_query_handler(func=lambda call: call.data == 'Today')
def call_math(call):
    call_timetable(call)


@bot.callback_query_handler(func=lambda call: call.data == 'Tomorrow')
def call_math(call):
    call_timetable(call)


@bot.callback_query_handler(func=lambda call: call.data == 'Week')
def call_math(call):
    call_timetable(call)


def log(message):
    print(datetime.now(),
          "Сообщение от {0} {1} {2} (id = {3}) : {4}".format(message.from_user.first_name, message.from_user.last_name,
                                                             message.from_user.username,
                                                             str(message.from_user.id), message.text))


def get_wind_direction(deg):
    l = ['С ', 'СВ', ' В', 'ЮВ', 'Ю ', 'ЮЗ', ' З', 'СЗ']
    for i in range(0, 8):
        step = 45.
        min = i * step - 45 / 2.
        max = i * step + 45 / 2.
        if i == 0 and deg > 360 - 45 / 2.:
            deg = deg - 360
        if min <= deg <= max:
            res = l[i]
            break

    return res


def get_weather(weather):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                           params={'id': config.city, 'units': 'metric', 'lang': 'ru', 'APPID': config.open_weather_id})
        data = res.json()
        weather += 'Погода в данный момент в городе {}: \n'.format(data['name'])
        weather += ('Температура: {}°, ощущается как {}°, {}, ветер{}.'.format('{0:+3.0f}'.format(data['main']['temp']),
                                                                               '{0:+3.0f}'.format(
                                                                                   data['main']['feels_like']),
                                                                               data['weather'][0]['description'],
                                                                               '{0:2.0f}'.format(data['wind'][
                                                                                                     'speed']) + ' м/с' + ' ' + get_wind_direction(
                                                                                   data['wind']['deg'])))
        return weather
    except Exception as e:
        print("Exception (weather):", e)
        pass


# Реализация отправки сообщения по расписанию
def call_course_sub(call):
    stud = Student(call.data)
    Students_dict[1] = stud

    course_sub(call)


def call_course_magistracy_sub(call):
    stud = Student(call.data)
    Students_dict[1] = stud

    course_magistracy_sub(call)


def subscription(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Подписаться', callback_data='sub_true'))
    keyboard.add(types.InlineKeyboardButton(text='Отписаться', callback_data='sub_false'))
    bot.send_message(message.from_user.id, text=config.sub, reply_markup=keyboard)


def sub_true(call):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text=config.groups[0], callback_data='Math_sub'))
    keyboard.add(types.InlineKeyboardButton(text=config.groups[1], callback_data='Pmi_sub'))
    keyboard.add(types.InlineKeyboardButton(text=config.groups[2], callback_data='MiMM_sub'))
    keyboard.add(types.InlineKeyboardButton(text=config.groups[3], callback_data='MiKN_sub'))
    keyboard.add(types.InlineKeyboardButton(text=config.groups[4], callback_data='MK_sub'))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Хорошо, теперь выбери направление подготовки и курс.', reply_markup=keyboard)


def course_sub(call):
    stud = Students_dict[1]

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='1', callback_data='1_sub'))
    keyboard.add(types.InlineKeyboardButton(text='2', callback_data='2_sub'))
    keyboard.add(types.InlineKeyboardButton(text='3', callback_data='3_sub'))
    keyboard.add(types.InlineKeyboardButton(text='4', callback_data='4_sub'))
    keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="Back_to_choose_sub"))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Ты выбрал направление подготовки - ' + config.groupsDict[
                              stud.table_group] + ', выбери курс:',
                          reply_markup=keyboard)


def course_magistracy_sub(call):
    stud = Students_dict[1]

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='1', callback_data='1'))
    keyboard.add(types.InlineKeyboardButton(text='2', callback_data='2'))
    keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="Back_to_choose_sub"))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Ты выбрал направление подготовки - ' + config.groupsDict[
                              stud.table_group] + ', выбери курс:',
                          reply_markup=keyboard)


def insert_sub(call):
    stud = Students_dict[1]
    stud.table_course = call.data

    with cx_Oracle.connect(config.orcl_user, config.orcl_password, config.orcl_dns, encoding="UTF-8") as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO subscription VALUES({}, '{}', '{}', {})".format(call.from_user.id,
                                                                                    call.from_user.first_name,
                                                                                    str(stud.table_group)[:-4],
                                                                                    str(stud.table_course)[:-4]))
        connection.commit()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Хорошо, я записал тебя.', )


@bot.callback_query_handler(func=lambda call: call.data == 'Back_to_choose_sub')
def call_math(call):
    sub_true(call)


@bot.callback_query_handler(func=lambda call: call.data == 'back_to_sub')
def call_math(call):
    subscription(call)


@bot.callback_query_handler(func=lambda call: call.data == 'sub_true')
def call_math(call):
    with cx_Oracle.connect(config.orcl_user, config.orcl_password, config.orcl_dns, encoding="UTF-8") as connection:
        cursor = connection.cursor()

        cursor.execute('select * from subscription where ИД={}'.format(call.from_user.id))
        result = cursor.fetchone()
        if result is None:
            sub_true(call)
        else:
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='back_to_sub'))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Ты уже подписан на рассылку.', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'sub_false')
def call_math(call):
    with cx_Oracle.connect(config.orcl_user, config.orcl_password, config.orcl_dns, encoding="UTF-8") as connection:
        cursor = connection.cursor()

        cursor.execute('select * from subscription where ИД={}'.format(call.from_user.id))
        result = cursor.fetchone()
        if result is None:
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='back_to_sub'))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Ты не подписан на рассылку.', reply_markup=keyboard)
        else:
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='back_to_sub'))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Ты успешно отписался. Больше ты не будешь получать рассылку.',
                                  reply_markup=keyboard)
            cursor.execute('delete from subscription where ИД={}'.format(call.from_user.id))
            connection.commit()


@bot.callback_query_handler(func=lambda call: call.data == '1_sub')
def call_math(call):
    insert_sub(call)


@bot.callback_query_handler(func=lambda call: call.data == '2_sub')
def call_math(call):
    insert_sub(call)


@bot.callback_query_handler(func=lambda call: call.data == '3_sub')
def call_math(call):
    insert_sub(call)


@bot.callback_query_handler(func=lambda call: call.data == '4_sub')
def call_math(call):
    insert_sub(call)


@bot.callback_query_handler(func=lambda call: call.data == "Math_sub")
def call_math(call):
    call_course_sub(call)


@bot.callback_query_handler(func=lambda call: call.data == 'Pmi_sub')
def call_math(call):
    call_course_sub(call)


@bot.callback_query_handler(func=lambda call: call.data == 'MiMM_sub')
def call_math(call):
    call_course_sub(call)


@bot.callback_query_handler(func=lambda call: call.data == 'MiKN_sub')
def call_math(call):
    call_course_sub(call)


@bot.callback_query_handler(func=lambda call: call.data == 'MK_sub')
def call_math(call):
    call_course_magistracy_sub(call)


def start_process():  # Запуск Process

    Process(target=P_schedule.start_schedule, args=()).start()


class P_schedule():  # Class для работы с schedule

    def start_schedule():  # Запуск schedule
        # Параметры для schedule
        schedule.every().day.at("07:00").do(P_schedule.every_day_timetable)

        while True:
            schedule.run_pending()
            time.sleep(1)

    # Функции для выполнения заданий по времени
    def every_day_timetable():
        with cx_Oracle.connect(config.orcl_user, config.orcl_password, config.orcl_dns, encoding="UTF-8") as connection:
            cursor = connection.cursor()
            cursor.execute("select * from subscription")
            for row in cursor:
                weather = ''
                stud = Student(row[2])
                Students_dict[0] = stud
                stud.id = row[0]
                stud.name = row[1]

                if stud.name is None:
                    stud.name = 'студент'

                stud.table_course = row[3]
                stud.string = 'Привет, {}❤\n\n'.format(stud.name)
                stud.string += get_weather(weather) + '\n\nРасписание на сегодня:'
                bot.send_message(stud.id, text=stud.string)
                step_one(datetime.today().isoweekday(), 0)
                bot.send_message(stud.id, text=stud.string)


if __name__ == '__main__':
    # Реализация отправки сообщения по расписанию
    start_process()

    bot.polling(none_stop=True)
