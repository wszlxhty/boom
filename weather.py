# -*- coding:utf-8 -*
import requests
import re
from bs4 import BeautifulSoup
import datetime
import time
import csv
import codecs
import pandas
import sys
import os
import pandas as pd
import threading
reload(sys)
sys.setdefaultencoding('utf-8')

class Weather_Crawler(object):
    def __init__(self):
        self.URL = 'http://m.weathercn.com/hourly-weather-forecast.do?partner=&language=zh-cn&id=2332753'

    def get_page(self):
        response = requests.get(self.URL)
        html = response.text
        self.soup = BeautifulSoup(html, "html.parser")

    def data_extract(self):
        self.list = []
        for i in range(1,24):
            try:
                hour_soup = self.soup.find_all('dl')[i] # 滚动时间，取值从当前时间的下一个整点一直到明天的这一个整点 列表取值范围 1~24
                detail_soup = self.soup.find_all('div', 'inner group')[i-1]  # 列表取值范围 0~23
                next_day = False
                date = datetime.date.today().strftime('%Y-%m-%d')  # 获取本地日期
                next_date = (datetime.date.today() + datetime.timedelta(days = 1)).strftime('%Y-%m-%d')
                hour = hour_soup.dt.contents[0]     # 获取网站时间
                today_time = datetime.datetime.strptime(date + ' ' + hour, '%Y-%m-%d %H:%M')
                nextday_time = datetime.datetime.strptime(next_date + ' ' + hour, '%Y-%m-%d %H:%M')
               # an_hour = time.strptime(datetime.timedelta(hours=1), '%H:%M:%S')
                an_hour = datetime.timedelta(hours=1)
                if today_time + an_hour < datetime.datetime.now():
                    next_day = True
                temperature = hour_soup.find_all('dd')[0].strong.contents[0]  # 温度
                weather = hour_soup.find_all('dd')[1].contents[0]  # 天气类型
                real_feel = detail_soup.find_all('li')[0].contents[1].strip()
                wind_direct = detail_soup.find_all('li')[1].contents[1].strip()
                real_wind_speed = detail_soup.find_all('li')[2].contents[1].strip()
                humidity = detail_soup.find_all('li')[3].contents[1].strip()
                dew_point = detail_soup.find_all('li')[4].contents[1].strip()
                cloudiness = detail_soup.find_all('li')[5].contents[1].strip()
                water_chance = detail_soup.find_all('li')[6].contents[1].strip()
                visibility = detail_soup.find_all('li')[7].contents[1].strip()
                self.list.append({'date':(next_date + ' ' + hour) if next_day else (date +' ' + hour), 'temperature':temperature, 'weather':weather,
                                            'real_feel':real_feel, 'wind_direct':wind_direct,
                                            'real_wind_speed':real_wind_speed, 'humidity':humidity,
                                            'dew_point':dew_point, 'cloudiness': cloudiness,
                                            'water_chance':water_chance, 'visibility':visibility,
                                            'timestamp':time.mktime(nextday_time.timetuple())
                                            })
            except:
                break
        self.df = pd.DataFrame(self.list)


    def update_CSV(self):
        orignal_data = pd.read_csv('data.csv', encoding='gb2312')
        timestamp = self.df.head().timestamp[0]
        new_data = orignal_data[orignal_data.timestamp <= timestamp] + self.df
        columns = ['date', 'temperature', 'weather', 'real_feel', 'wind_direct', 'real_wind_speed',
                   'humidity', 'dew_point', 'cloudiness', 'water_chance', 'visibility','timestamp']
        new_data.iloc[:,1:].to_csv('data.csv', encoding='gb2312', columns=columns)
        self.df.to_csv('data.csv', encoding='gb2312', columns=columns)

    def operate(self):
        while True:
            self.get_page()
            self.data_extract()
            self.update_CSV()



instance = Weather_Crawler()
while True:
    instance.operate()
    time.sleep(1200)











