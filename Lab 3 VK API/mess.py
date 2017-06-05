from itertools import count
from urllib import response
from pprint import pprint as pp
from datetime import datetime
import requests


def messages_get_history(user_id=32259366, offset=0, count=200):
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "user_id must be positive integer"
    assert count >= 0, "user_id must be positive integer"

    domain = "https://api.vk.com/method"
    access_token = '1ea84a5a422285c7878d7a7f8d62636db5e8e43344efe23816c466da80dcd5f3382f232b4f63e6cd58db0'
    user_id = 32259366

    query_params = {
        "domain": domain,
        "access_token": access_token,
        "user_id": user_id,
        "offset": offset,
        "count": count
    }

    query = "{domain}/messages.getHistory?access_token={access_token}&user_id={user_id}&offset={offset}&count={count}&v=5.53".format(**query_params) # запрос
    response = requests.get(query)
    return response.json()

def count_dates_from_messages():
    history = messages_get_history(32259366)
    dates =[]
    count = history['response']['count']
    if count > 200:
        count = 200
    for i in range(count):
        message = history['response']['items'][i]
        date = datetime.fromtimestamp(message['date']).strftime("%Y-%m-%d") # меняет формат даты
        dates.append(date)

    from collections import Counter #вид словаря, который позволяет нам считать количество неизменяемых объектов
    from operator import itemgetter

    data_count = Counter(dates)
    data_count = list(data_count.items())
    data_count.sort(key=itemgetter(0))
    key = []
    values =[]
    for i in data_count:
        key.append((i[0]))
        values.append(i[1])
    return key, values


import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from datetime import datetime

plotly.tools.set_credentials_file(username='talekaterina', api_key='EQJSJraQeiJ2HvtiXCMz')

x = count_dates_from_messages()[0]
y = count_dates_from_messages()[1] # кол-во сообщений в день

#x = [datetime(year=2016, month=12, day=3),
#     datetime(year=2016, month=12, day=4),
#     datetime(year=2016, month=12, day=5)]
#y=[200, 50, 10]

data = [go.Scatter(x=x,y=y)]
py.plot(data)
pp(count_dates_from_messages())

