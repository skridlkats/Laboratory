import requests
from bs4 import BeautifulSoup
from bottle import route, run, template, request, redirect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

r = requests.get("https://news.ycombinator.com/newest")
page = BeautifulSoup(r.text, 'html.parser')
new_list = []


news_kol = len(page.findAll(attrs={"class":"athing"}))
for i in range(10):
    author = page.findAll(attrs={"class":"hnuser"})[i].string
    #comments = page.findAll(attrs={"href":"item?id="})[i].string[:-3]
    points = page.findAll(attrs={"class":"score"})[i].string[:-6]
    title = page.findAll(attrs={"class":"storylink"})[i].string
    url = page.findAll(attrs={"class":"sitestr"})[i].string
    new_list.append({
        'author': author,
        #'comments': comments,
        'points': points,
        'title': title,
        'url': url
        })
#print(new_list)

Base = declarative_base()

class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key = True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)

engine = create_engine("sqlite:///news.db")
Base.metadata.create_all(bind=engine)
session = sessionmaker(bind=engine)
s = session()

#Добавление новостей в бд
for i in new_list:
   n = News(**i)
   s.add(n)
   s.commit()


s = session()
kol_news = len(s.query(News).filter(News.label != None).all())
kol_good = len(s.query(News).filter(News.label == 'good').all())
good = kol_good/kol_news
#print('Вероятность встретить интересные новости: ',good)


s = session()
kol_news = len(s.query(News).filter(News.label != None).all())
kol_maybe = len(s.query(News).filter(News.label == 'maybe').all())
may = kol_maybe/kol_news
#print( 'Вероятность встретить новости, которые понравятся: ', may)


kol_news = len(s.query(News).filter(News.label != None).all())
kol_never = len(s.query(News).filter(News.label == 'never').all())
never = kol_never/kol_news
#print('Вероятность встретить неинтересные новости: ',never)


s = session()
dict_good = dict()
kol_words = 0
news_good = s.query(News).filter(News.label == 'good').all()
for i in news_good:
    words = i.title.split()
    for l in words:
        kol_words += 1
  # словарь с частотой слов в классе
for ne in news_good:
    words = ne.title.split()
    for i in words:
        if i not in dict_good:
            dict_good[i] = 1
        else:
            dict_good[i] += 1
#count_words_news_good = sum(dict_good.values())  # кол-во слов в классе
for i in dict_good:  # получаю словарь с вероятностью слова в классе
    dict_good[i] = round(dict_good[i] / kol_words, 5)
#print( dict_good)


s = session()
news_maybe = s.query(News).filter(News.label == 'maybe').all()
dict_maybe = dict()
for ne in news_maybe:
    words = ne.title.split()
    for i in words:
        if i not in dict_maybe:
            dict_maybe[i] = 1
        else:
            dict_maybe[i] += 1
count_words_news_maybe = sum(dict_maybe.values())
for i in dict_maybe:
    dict_maybe[i] = round(dict_maybe[i] / count_words_news_maybe, 5)
#print( dict_maybe)

s = session()
news_never = s.query(News).filter(News.label == 'never').all()
dict_never = dict()
for ne in news_never:
    words = ne.title.split()
    for i in words:
        if i not in dict_never:
            dict_never[i] = 1
        else:
            dict_never[i] += 1
count_words_news_never = sum(dict_never.values())
for i in dict_never:
    dict_never[i] = round(dict_never[i] / count_words_news_never, 5)
#print( dict_never)


new_news = s.query(News).filter(News.label == None).all()
g, m, n = 0, 0, 0
listg=[]
listm=[]
listn=[]
for i in new_news:
    new_words = i.title.split()
    for j in new_words:
        if j in dict_good:
            g += 1
        elif j in dict_maybe:
            m += 1
        elif j in dict_never:
            n += 1
    prod_g = good + g
    prod_m = may + m
    prod_n = never + n
    if prod_g > prod_m:
        if prod_g > prod_m:
            listg.append(i)
        else:
            listn.append(i)
    else:
        if prod_m> prod_n:
            listm.append(i)
        else:
            listn.append(i)
#print(listn, listm,listg)


# if prod_g > prod_m:
#     if prod_g > prod_n:
#         listg.append(i)
#     else:
#         listn.append(i)
# else:
#     if prod_m > prod_n:
#         listm.append(i)
#     else:
#         listn.append(i)
# print(listg, listm, listn)


#@route('/')
@route('/probability_news')
def news_list():
    s = session()
    #f = probability_new_news()
    rows = s.query(News).filter(News.label == None).all()
    rows_good = listg
    rows_maybe = listm
    rows_never = listn
    #return template('news_template', rows_good=listg, rows_maybe=listm, rows_never=listn)

# @route('/')
# @route('/news')
# def news_list():
#     s = session()
#     rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows_good)

@route('/add_label/')
def add_label():
    # 1. Получить значения параметров label и id из GET-запроса
    # 2. Получить запись из БД с соответствующим id (такая запись только одна!)
    # 3. Изменить значение метки записи на значение label
    # 4. Сохранить результат в БД

    s = session()
    label = request.query.label
    id = request.query.id
    i = s.query(News).filter(News.id == id).first()
    i.label = label
    s.commit()
    redirect('/news')

@route('/update_news')
def update_news():
    # 1. Получить данные с новостного сайта
    # 2. Проверить каких новостей еще нет в БД. Будем считать,
    #    что каждая новость может быть уникально идентифицирована
    #    по совокупности двух значений: заголовка и автора
    # 3. Сохранить в БД те новости, которых там нет
    s = session()
    r = requests.get("https://news.ycombinator.com/news?p=1")
    #new_news = get_news(r.text)
    for i in new_list:
        if not s.query(News).filter(News.title == i['title'] and News.author == i['author']).all():
            n = News(**i)
            s.add(n)
            s.commit()
    redirect('/news')


# http://localhost:8080/news
run(host='localhost', port=8080)

