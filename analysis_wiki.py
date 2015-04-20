# JohnHook
# 19.04.15

import urllib.request  # для просмотра исходного кода интернет страницы
import re

get_list = lambda foo, url: foo.findall(
    str(urllib.request.urlopen(url).read()))  # список свех подстрок страницы url удовлетворяющих кортежу foo
correct = lambda l: list(
    map(lambda s: 'http://af.wikipedia.org' + s[0:-1] + s[-1], l))  # приводит список ссылок к нормальному виду
del_amp = lambda s: s[0:64] + s[68:-1] + s[-1]  # удаляет amp;
del_a = lambda l: list(map(lambda s: [s, s[0:-4]][s[-1] == '>'], l))  # удаляет </a>

table = re.compile('<table( *\w* *= *"[^"]*")*>', re.IGNORECASE)  # кортеж table
site = re.compile('/wiki/[^"]*', re.IGNORECASE)  # кортеж url-адресса
next_page = re.compile('/w/index.php\?title=Spesiaal:Alle_bladsye&amp;from=[^"]*',
                       re.IGNORECASE)  # кортеж кандитата на страницу со списком следующих статей

calc = lambda url: len(get_list(table, url))  # кол-во таблиц на странице
site_list = lambda url: del_a(correct(get_list(site, url)))  # список всех ссылок на странице
site_next = lambda url: del_amp(correct(get_list(next_page, url))[2])  # адресс следующей страницы со списком статей

res = {}  # словарь [страница:кол-во таблиц]
t = 0  # номер проверяемой страницы (убрать)


def list_processing(act):  # подсчет страницы
    for i in site_list(act):  # проходимся по всем ссылкам на данной странице
        if i not in res:  # если мы тут еще не были
            try:  # страница может не существовать
                global t  # (убрать)
                t += 1  # поддержка счетчика (убрать)
                print(str(t) + '::' + i)  # вывод информации (убрать)
                res[i] = calc(i)  # занесение страницы в словарь
            except:
                print('ERROR::' + i)  # вывод ошибки (убрать)
                pass


act = 'http://af.wikipedia.org/w/index.php?title=Spesiaal%3AAlle+bladsye&from=%21'  # первая страница со списком статей
arr = ['', '']  # для проверки на зацикливание

while not act == arr[0]:  # пока мы еще не зациклились
    print(act)  # вывод информации (убрать)
    list_processing(act)  # расчет для каждой статьи из списка
    arr[0], arr[1], act = arr[1], act, site_next(
        act)  # переход на следующий список и обновление массива для проверки зацикливания

top = list(res.items())  # создаем топ
top.sort(key=lambda x: -x[1])  # сортируем его

f = open('res.html', 'w')
for i in top[0:30]:
    f.write(str(i[1]) + '::' + str(i[0]) + '\n')  # выводим информацию в res.html
f.close()