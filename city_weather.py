import base64
from requests import Session
import datetime
import time
import json
import os

url = 'http://www.aqistudy.cn/html/city_detail.html?v=1.8'
data_url = 'http://www.aqistudy.cn/api/getdata_cityweather.php'
s = Session()
s.get(url)

filename = '2016baoding_weather.csv'
if not os.path.exists(filename):
	f = open(filename,'w+')
	f.close()
# ----------------**********------------------------
startday = datetime.datetime(2016,1,1)
endday = datetime.datetime(2016,9,23)
# ----------------**********------------------------
oneday = datetime.timedelta(days = 1)
day = startday

while day < endday:
	print day
	time.sleep(10)
	endTime = day + oneday
	startTime = base64.b64encode(str(day))
	endTime = base64.b64encode(str(endTime))
	day = day + oneday
	postdata = {
		'city':'5L+d5a6a',# baoding
		# 'city':'5YyX5Lqs', # beijing
		'type':'SE9VUg==',
		'startTime':startTime,
		'endTime':endTime
		}
	
	data = s.post(data_url,data = postdata).text
	print data
	city_weather = base64.b64decode(base64.b64decode(data))
	# print city_weather[::-3]

	# print json.dumps(data,indent=4)
	try:
		data = json.loads(city_weather[0:-6])
		# json.dump(data,indent=4)
		for item in data['rows']:
			times = item['time']
			fengji = item['wse']
			wendu = item['temp']
			shidu = item['humi']
			with open(filename,'a+') as fhand:
				temp = '%s,%s,%s,%s,\n' %(times,fengji,wendu,shidu)
				fhand.write(temp)
	except:
		try:
			data = json.loads(city_weather)
			# json.dump(data,indent=4)
			for item in data['rows']:
				times = item['time']
				fengji = item['wse']
				wendu = item['temp']
				shidu = item['humi']
				with open(filename,'a+') as fhand:
					temp = '%s,%s,%s,%s,\n' %(times,fengji,wendu,shidu)
					fhand.write(temp)
		except:
			print 'fuck'
	# print json.dumps(data,indent = 4)
