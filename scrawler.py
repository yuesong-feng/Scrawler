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


urls = getlinks('2020-08-01', '2020-09-01', 'places.txt')

i = 0
while i < len(urls):
    if not os.path.exists(urls[i][31:38] + '-' + urls[i][52:63] + '.html'):
        browser = webdriver.Edge('C:/Users/yuesong-feng/PycharmProjects/crawler/venv/Scripts/msedgedriver.exe')
        browser.get(urls[i])
        with open(urls[i][31:38] + '-' + urls[i][52:63] + '.html', 'w', encoding='utf-8')as f:
            f.write(browser.page_source)
        browser.close()
    i += 1
