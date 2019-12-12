# -*- coding: utf-8 -*-
import time
from bs4 import BeautifulSoup
from io import open
import pandas as pd
import random, requests
import DAN

region = 'Tainan'
url = 'https://www.cwb.gov.tw/V7/observe/24real/Data/46741.htm'


def f(url, fn):
	headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
	}
	res = requests.get(url, headers=headers)
	res.encoding = 'utf-8'

	open(fn,'wb').write(res.text.encode('utf-8'))

fn = region+ '.html'.format(0,0)
f(url, fn)

def get_element(soup, tag, class_name):
    data = []
    table = soup.find(tag, attrs={'class':class_name})
    rows = table.find_all('tr')
    del rows[0]
    
    for row in rows:
        first_col = row.find_all('th')
        cols = row.find_all('td')
        cols.insert(0, first_col[0])
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele]) 
    return data

region ='Tainan'
   
file_name = region+".html"

f = open (file_name,'r', encoding='utf-8')
s = f.readlines()
s = ''.join(s)

soup = BeautifulSoup(s, "lxml")

df_tmp = get_element(soup, 'table','BoxTable')

print(df_tmp)


df = pd.DataFrame(df_tmp) 

temperature = df.iloc[0,1]
wind_direction = df.iloc[0,4]
wind_speed = df.iloc[0,5]
temp_wind = df.iloc[0,6]
humid = df.iloc[0,8]
rain = df.iloc[0,10]


print('temparature:',temperature)

ServerURL = 'https://6.iottalk.tw' #with SSL connection
Reg_addr = 'hank230201' #if None, Reg_addr = MAC address

DAN.profile['dm_name']='hank_weather3'
DAN.profile['df_list']=['Temperature','Windspeed','winddirection','presentwind','Humidity','rain',
            'Humidity-O', 'WindSpeed-O', 'Temperature-O', 'RainMeter-O', 'WindDirection-O', 'PresentWind-O']
#DAN.profile['df_list']=['Temperature','Windspeed','winddirection','presentwind','Humidity','rain']

DAN.device_registration_with_retry(ServerURL, Reg_addr)
#DAN.deregister()  #if you want to deregister this device, uncomment this line
#exit()            #if you want to deregister this device, uncomment this line
temp=0
while True:
    try:
        DAN.push ('Temperature', temperature) #Push data to an input device feature "Dummy_Sensor"
        DAN.push ('winddirection', wind_direction)
        DAN.push ('Windspeed', wind_speed[0:3])
        DAN.push ('presentwind', temp_wind)
        DAN.push ('Humidity', humid)
        DAN.push ('rain', rain)
        #==================================

        """data1 = DAN.pull('Temperature-O')#Pull data from an output device feature "Dummy_Control"
        data2 = DAN.pull('WindDirection-O')
        data3 = DAN.pull('WindSpeed-O')
        data4 = DAN.pull('PresentWind-O')
        data5 = DAN.pull('Humidity-O')
        data6 = DAN.pull('RainMeter-O')
        print('溫度:',data1)
        print('風向:',data2)
        print('風力:',data3)
        print('陣風:',data4)
        print('濕度:',data5)
        print('雨量:',data6)
        time.sleep(2)"""
        
    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)    

    time.sleep(0.2)

#########################################################################################
#import pandas as pd
    print ('Region :', region,'Building table ...')
    col_list = ['觀測時間', '溫度(°C)', '溫度(°F)', '天氣', '風向', '風力 (m/s)|(級)', '陣風 (m/s)|(級)', '能見度(公里)', '相對溼度(%)', '海平面氣壓(百帕)', '當日累積雨量(毫米)', '日照時數(小時)']
    df = pd.DataFrame(columns = col_list)
    df_tmp = pd.DataFrame(df_tmp)
    df_tmp.columns = col_list
    df = pd.concat([df, df_tmp], axis=0)   
    df = df.reset_index(drop=True)    
    df.to_csv(( region + '.csv'), encoding = 'utf-8')



