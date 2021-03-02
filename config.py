﻿orcl_user = 'login'  # Логин пользователя базы данных
orcl_password = 'password'  # Пароль пользователя базы данных
orcl_dns = 'hostname/service_name'  # Указать свои данные

token = 'Your token'  # Токен вашего telegram-бота.

open_weather_id = 'Your token'  # Токен с OpenWeather https://openweathermap.org/
city = 000000  # Можно узнать с https://openweathermap.org/city/524901, где последнее - id города

groups = ['Математика', 'Прикладная математика и информатика', 'Механика и математическое моделирование',
          'Математика и компьютерные науки', 'Математическая кибернетика']

groupsDict = {'Math': 'Математика', 'Pmi': 'Прикладная математика и информатика',
              'MiMM': 'Механика и математическое моделирование',
              'MiKN': 'Математика и компьютерные науки', 'MK': 'Математическая кибернетика',
              'Math_sub': 'Математика', 'Pmi_sub': 'Прикладная математика и информатика',
              'MiMM_sub': 'Механика и математическое моделирование',
              'MiKN_sub': 'Математика и компьютерные науки', 'MK_sub': 'Математическая кибернетика'
              }

time = '1 пара - 8:00-9:30\n' \
       '2 пара - 9:40-11:10\n' \
       'Обеденный перерыв 30 минут\n' \
       '3 пара - 11:40-13:10\n' \
       '4 пара - 13:20-14:50\n' \
       'Перерыв между сменами 20 минут\n' \
       '5 пара - 15:10-16:40\n' \
       '6 пара - 16:50-18:20\n' \
       '7 пара - 18:30-20:00\n' \
       '8 пара - 20:10-21:40'

groups_data = 'БАКАЛАВРИАТ\n\n''Математика\n' \
              '------------------------------------------------------\n' \
              'Прикладная математика и информатика\n' \
              '------------------------------------------------------\n' \
              'Механика и математическое моделирование\n' \
              '------------------------------------------------------\n' \
              'Математика и компьютерные науки\n' \
              '------------------------------------------------------\n' \
              'МАГИСТРАТУРА\n\n' \
              'Математическая кибернетика'

greeting = 'Привет! Я бот-расписание УдГУ, ИМИТиФ, Математический факультет. ' \
           'Напиши мне "/" и я покажу, что я умею.'

space = '------------------------------------------------------'

days_of_week = {1: 'Понедельник', 2: 'Вторник', 3: 'Среда', 4: 'Четверг', 5: 'Пятница', 6: 'Суббота', 7: 'Воскресенье'}

table = {'Math': 'МАТ', 'Pmi': 'ПМИ', 'MiMM': 'МиММ', 'MiKN': 'МиКН', 'MK': 'МК',
         'Math_sub': 'МАТ', 'Pmi_sub': 'ПМИ', 'MiMM_sub': 'МиММ', 'MiKN_sub': 'МиКН', 'MK_sub': 'МК',
         1: 'ПН', 2: 'ВТ', 3: 'СР', 4: 'ЧТ', 5: 'ПТ', 6: 'СБ', 7: 'ВС'}

sub = "Ты можешь сделать так, чтобы кажое утро в 7:00 я отправлял тебе расписание на сегодня. Для этого нажми кнопку" \
      " подписаться или отписаться, если ты не хочешь больше получать сообщения."