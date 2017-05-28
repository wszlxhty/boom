# -*- coding:utf-8 -*
#要在文件中写中文，必须加上面那句话，否则默认使用ascll编码
import re
import requests
import os
from bs4 import BeautifulSoup
pathnow = os.getcwd()


class pic91(object):
    def __init__(self,PageRange):
        self.homeurl = 'http://91.t9m.space/forumdisplay.php?fid=19&page='
        self.topiclist = []
        self.PageRange = PageRange

    def operate(self):
        self.gen_url()
        for item in self.topiclist:
            self.get_pic(item)

    def gen_url(self):
        for page in range(self.PageRange[0],self.PageRange[1]+1):
            URL = self.homeurl + str(page)
            response = requests.get(URL)
            response.encoding = 'utf-8'  ###抓取时候先将网页重新编码，从header信息获得编码方式
            html = response.text
            soup = BeautifulSoup(html)
            pattern = re.compile('normalthread.*?')
            total = soup.find_all(id=pattern)  ##beautifulsoup抓取多级节点中的内容，先用find_all找出某一级的特征
            for item in total:  ##可以使用简单的参数，也可以使用正则表达式
                self.topiclist.append('http://91.t9m.space/'+item.a.get('href'))  ##find_all返回一个bs4对象，可以继续用单层bs的方法去提取节点信息

    def get_pic(self, PageUrl):
        response = requests.get(PageUrl)
        response.encoding = 'utf-8'     ###抓取时候先将网页重新编码，从header信息获得编码方式
        html = response.text
        pattern = re.compile('<img src=".*?" file="(.*?)" width.*?>')  ##正则表达式抓取图片URL
        result = re.findall(pattern, html)
        pattern = re.compile('<title>(.*?)</title>')                    ##正则表达式抓取标题命名文件夹
        title = re.search(pattern, html)
        newfolder = pathnow + "\\" + self.name_process(title.group(1))
        try:
            os.mkdir(newfolder)          #建立重复文件夹会引发Windows error
        except:
            print 'Already have'
        os.chdir(newfolder)
        for i in range(len(result)):
            picurl = 'http://91.t9m.space/' + result[i]
            self.saveImg(picurl, str(i))
        os.chdir(pathnow)


    def saveImg(self, imageURL, fileName):
        data = requests.get(imageURL,stream=True)     #请求多媒体文件
        suffixPattern = re.compile('\.(\w{3})')       #匹配文件格式
        suffix = re.findall(suffixPattern, imageURL)
        f = open(fileName + '.'+ suffix[-1], 'wb')     #文件名称加后缀
        f.write(data.content)
        f.close()

    def log(self,context):
        f = open('record.txt', 'w')
        f.write('cctv')
        f.close()

    def name_process(self,text):
        a = re.split(':',text)
        a = ''.join(a)
        a = re.split('/', a)
        a = ''.join(a)
        a = re.split('\?', a)
        a = ''.join(a)
        a = re.split('<', a)
        a = ''.join(a)
        a = re.split('>', a)
        a = ''.join(a)
        a = re.split('"', a)
        a = ''.join(a)
        return a
page1 = raw_input('start page: ')
page2 = raw_input('finish page: ')
master = pic91([int(page1),int(page2)])
master.operate()


