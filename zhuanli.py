# -*- coding:utf-8 -*
import re
import requests
import os
from bs4 import BeautifulSoup
import datetime
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
pathnow = os.getcwd()

class ncepu_zhuanli(object):
    def __init__(self,TimeRange):
        self.homeurl = 'http://59.67.225.72/ky/Research/IPR-print.asp?sqbh='
        self.datelist = []
        self.timeRange = TimeRange

    def get_info(self):
        pre_response = requests.get('http://59.67.225.72/ky/Research/IPR-browse.asp#userconsent#')
        cookies = pre_response.cookies
        for date in self.datelist:
            for num in range(1,50):
                URL = self.homeurl + str(date) +'-' +str(num)
                response = requests.get(URL,cookies=cookies)
                if response.status_code == 200: 
                    html = response.text.encode('ISO-8859-1').decode(requests.utils.get_encodings_from_content(response.text)[0],'ignore')
                    self.info_process(html, str(date) +'-' +str(num))
                    print URL
                elif response.status_code == 500:
                    pass#print 500
                else:
                    pass#print 'wrong'

    def info_process(self, html, number):
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find('table',border="1px").find_all('tr')   
        linelist = []
        f = open('zhuanli.txt', 'a')
        f.write('-----------------------------------' +number + '------------------------------------------\n')
        for i in range(6):
            text1 = items[i].find_all('td')[0].text.strip()
            if len(items[i].find_all('td'))>1:
                text2 = items[i].find_all('td')[1].text.strip()
                f.write(text1 +': '+ text2+'\n')
            else:
                f.write(text1+'\n')
        f.close()

    def time_gen(self):
        date1 = datetime.datetime.strptime(str(self.timeRange[0]), '%Y%m%d')
        date2 = datetime.datetime.strptime(str(self.timeRange[1]), '%Y%m%d')
        delta = date2 - date1
        for i in range(delta.days+1):
            self.datelist.append((date1 + datetime.timedelta(days=i)).strftime('%Y%m%d'))

    def operate(self):
        self.time_gen()
        self.get_info()
time1 = raw_input(u'按照20110101的格式输入起始时间: ')
time2 = raw_input(u'按照20110101的格式输入结束时间: ')
master = ncepu_zhuanli([time1,time2])
master.operate()


