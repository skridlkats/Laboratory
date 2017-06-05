from itertools import count
from urllib import response
from pprint import pprint as pp
from datetime import datetime
import requests


def get_friends(user_id, fields):
    assert isinstance(user_id, int), "user_id must be positive integer" #проверка значений
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"

    domain = "https://api.vk.com/method"
    access_token = '1ea84a5a422285c7878d7a7f8d62636db5e8e43344efe23816c466da80dcd5f3382f232b4f63e6cd58db0'
    user_id = 49136318

    query_params = {
        "domain": domain,
        "access_token": access_token,
        "user_id": user_id,
        "fields": fields
    }

    query = "{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v=5.53".format(**query_params)
    response = requests.get(query)

    data = []
    for i in range(response.json()['response']['count']):
        try:
            if len(response.json()['response']['items'][i]['bdate']) > 8:
                data.append(response.json()['response']['items'][i]['bdate'])
        except KeyError:
            pass
        except IndexError:
            pass
    return data



def age_predict(user_id):
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"

    data_1 = get_friends(32259366, 'bdate')
    year = []
    for i in range(len(data_1)):
        year.append((str(data_1[i]).split('.'))[2])
    age = []
    for i in range(len(year)):
        age.append(2016 - int(year[i]))
    age_user = int(sum(age) / len(age))
    return age_user
print(age_predict(32259366))