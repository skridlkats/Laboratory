import telebot
import requests
import config
from bs4 import BeautifulSoup
from datetime import datetime

bot = telebot.TeleBot(config.token)

def get_page(group, week=''):
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.domain, # сайт Итмо, ктотор находится в сонф
        week=week,
        group=group)
    response = requests.get(url) # интернет запрос
    web_page = response.text
    return web_page

def get_schedule(web_page, day):
    soup = BeautifulSoup(web_page, "html5lib") # принимает HTML док в виде строки, анализирует док и создает соответствующую структуру данных в памяти.

    # Получаем таблицу с расписанием на day
    schedule_table = soup.find("table", attrs={"id": "{}day".format(day)})

    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    #Кабинеты
    cabs_list = schedule_table.find_all('dd', attrs={"class": "rasp_aud_mobile"})
    cabs_list = [cab.text for cab in cabs_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

    return times_list, cabs_list, locations_list, lessons_list

day_num_list={'1':'monday' ,'2':'tuesday','3':'wednesday','4':'thursday','5':'friday','6':'saturday'}

#расписание занятий в указанный день
@bot.message_handler(commands=['monday','tuesday','wednesday','thursday','friday','saturday']) # Обработчик команд
def get_timetable(message):
    _, week,group = message.text.split(' ')
    day=_.split('/')[1]

    web_page = get_page(week,group)
    times_lst, locations_lst, lessons_lst = get_schedule(web_page,day)

    resp = ''
    for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')

# Распмсание на завтра
@bot.message_handler(commands=['tomorrow'])
def get_timetable(message):
    _, group = message.text.split()

    day_num=int(datetime.today().isoweekday())   #номер недели (от 1 до 7) дни недели
    week = int(datetime.today().strftime('%W'))
    if week%2==0:
        week=str(1)  # четная неделя
    else:
        week=str(2)
    if day_num !=7:
        day=day_num_list[str(day_num+1)]
        week=str(week)
    else:
        day=day_num_list[str(day_num)]
    web_page = get_page(group,week)
    times_lst, locations_lst, lessons_lst = get_schedule(web_page,day)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')

#Выводит все расписание
@bot.message_handler(commands=['all'])
def get_timetable(message):
    _, week, group = message.text.split(' ')
    web_page = get_page(week,group)
    days=['monday','tuesday','wednesday','thursday','friday','saturday']
    for day in days:
        times_lst, locations_lst, lessons_lst, _ = get_schedule(web_page, day)
        resp = ''
        resp += day.upper()
        for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
           resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
        bot.send_message(message.chat.id, resp, parse_mode='HTML')

if __name__ == '__main__':      # бот должен не прекращать работу при возникновении ошибок
    bot.polling(none_stop=True)