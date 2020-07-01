import re

from selenium import webdriver
import arrow
import datetime
import os


def getroues(file):
    with open(file, 'r') as f:
        city = []
        for line in f.readlines():
            city.append(line.strip('\n'))
    routes = []
    m = 0
    n = 0
    while m < len(city):
        while n < len(city):
            if n == m:
                n += 1
                continue
            ##
            routes.append(city[m] + '-' + city[n])
            ##
            n += 1
        n = 0
        m += 1
    return routes


def getlinks(startdate, enddate, places):
    a = 0
    all_date_list = []
    date1 = datetime.datetime.strptime(startdate, "%Y-%m-%d")
    date2 = datetime.datetime.strptime(enddate, "%Y-%m-%d")
    days_sum = (date2 - date1).days
    while a < days_sum:
        b = arrow.get(startdate).shift(days=a).format("YYYY-MM-DD")
        a += 1
        all_date_list.append(b)

    routes = getroues(places)
    k = 0
    allroutes = []
    while k < len(routes):
        allroutes.append('https://www.meituan.com/flight/' + routes[k] + '/?forwardDate=')
        k += 1
    alldatesurl = []
    url_sum = len(allroutes) * days_sum
    i = 0
    j = 0
    while i < len(allroutes):
        while j < len(all_date_list):
            alldatesurl.append(allroutes[i] + all_date_list[j])
            j += 1
        j = 0
        i += 1
    return alldatesurl


urls = getlinks('2020-06-15', '2020-07-01', 'places.txt')
i = 0
while i < len(urls):
    if os.path.exists(urls[i][31:38] + '-' + urls[i][52:63] + '.html'):
        with open(urls[i][31:38] + '-' + urls[i][52:63] + '.html', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        with open(urls[i][31:38] + '-' + urls[i][52:63] + '.txt', 'w', encoding='utf-8') as f_w:
            for line in lines:
                if "ac-name-text" in line:
                    f_w.write(line)
                if "price-btn-text" in line:
                    f_w.write(line)
    i += 1
i = 0
while i < len(urls):
    if os.path.exists(urls[i][31:38] + '-' + urls[i][52:63] + '.txt'):
        results = []
        with open(urls[i][31:38] + '-' + urls[i][52:63] + '.txt', 'r', encoding='utf-8')as f:
            f.readline()
            f.readline()
            lines = f.readlines()
            for line in lines:
                line = re.sub('\\<.*?\\>','',line)
                line = re.sub('&nbsp','',line)
                line = re.sub('日一二三四五六.*价格','',line)
                line = re.sub('直飞', '', line)
                line = re.sub('票少', '', line)
                line = re.sub('特惠', '', line)
                line = re.sub(' ', '', line)
                line = re.sub('耗时短', '', line)
                line = re.sub('最低价', '', line)
                results.append(line)
        with open(urls[i][31:38] + '-' + urls[i][52:63] + '.txt', 'w', encoding='utf-8')as f_w:
            for result in results:
                f_w.write(result)
    i += 1

i = 0
with open('datas.txt', 'w', encoding='utf-8')as datas:
    while i < len(urls):
        if os.path.exists(urls[i][31:38] + '-' + urls[i][52:63] + '.txt'):
            with open(urls[i][31:38] + '-' + urls[i][52:63] + '.txt', 'r', encoding='utf-8')as f:
                datas.write(urls[i][31:38] + ' ' + urls[i][52:63] + ' ')
                line1 = f.readline()
                index1 = line1.find(';')
                datas.write(line1[4:8]+' '+line1[8:index1]+' '+line1[index1+1:index1+6]+' ')
                index2 = line1.find(':', line1.find(':')+1)
                datas.write(line1[index2-2:index2+3]+' ')
                line2 = f.readline()
                datas.write(line2[1:line2.find('起')]+'\n')
        i += 1
