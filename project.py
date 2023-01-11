# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 13:27:21 2021
@author: Administrator
"""


##
import pandas as pd
import requests
import xlwings as xw #excel套件
import matplotlib.pyplot as plt

#網址可改日期
url = 'https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=20211223&type=ALL'
res = requests.get(url)
data = res.text
print(data)

data.split('\n')

type(data.split('\n'))
#數字可能會變 要測一下
data.split('\n')[-989]

for da in data.split('\n'):
    if len(da.split('","')) == 16 and da.split('","')[0][0] != '=':
        print(da.split('","'))
        
cleaned_data = []
for da in data.split('\n'):
    if len(da.split('","')) == 16 and da.split('","')[0][0] != '=':
        cleaned_data.append([ele.replace('",\r','').replace('"','') 
                             for ele in da.split('","')])
df = pd.DataFrame(cleaned_data, columns = cleaned_data[0])
df = df.set_index('證券代號')[1:]
xw.view(df)  


##存入資料庫
import sqlite3
import csv


with open('活頁簿3.csv', encoding='ANSI') as file:
    csvReader=csv.reader(file)
    data=list(csvReader)

conn = sqlite3.connect('即時股價2.db')
cursor = conn.cursor()

sql='CREATE TABLE IF NOT EXISTS stock9 \
    ("證券代號"TEXT,"證券名稱"TEXT,"成交股數"TEXT,"成交金額"TEXT,"漲跌(+/-)"TEXT,"漲跌價差"TEXT,"本益比"TEXT)'
conn.execute(sql)

for i in data:
    sql='''INSERT INTO stock9("證券代號","證券名稱","成交股數","成交金額","漲跌(+/-)","漲跌價差","本益比") VALUES ('{}','{}','{}','{}','{}','{}','{}')'''
    sql= sql.format(i[0],i[1],i[2],i[4],i[10],i[11],i[15])
    conn.execute(sql)

    
conn.commit()
conn.close()

##資料分析

#將千分位去掉 
df=df.applymap(lambda x:x.replace(',','') )
#轉換成數字
df['成交股數'].astype('int')
df['成交股數'] = df['成交股數'].astype('int')

#成量排行
df2=df.iloc[:,0:2]
df3=df2.sort_values('成交股數',ascending=False)

df3.index.names = [None]

print('成量排行:\n',df3)
print('成量排行:\n',df3.head(50))

#畫圖用
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

df13=df3.head(5)  
a=df13.plot(kind='bar')
font=FontProperties(fname=r'\Windows\Fonts\msjh.ttc')
plt.xlabel('證券名稱',fontproperties=font)
plt.legend(prop=font)
plt.show()

#成值排行
df['成交金額'].astype('float')
df['成交金額'] = df['成交金額'].astype('float')

df4=df.iloc[:,[0,3]]
df5=df4.sort_values('成交金額',ascending=False)

df5.index.names = [None]

print('成值排行:\n',df5)
print('成值排行:\n',df5.head(50))

df14=df5.head(5)
a=df14.plot(kind='bar')
font=FontProperties(fname=r'\Windows\Fonts\msjh.ttc')
plt.xlabel('證券名稱',fontproperties=font)
plt.legend(prop=font)
plt.show()
 

#漲價排行
df['漲跌價差'].astype('float')
df['漲跌價差'] = df['漲跌價差'].astype('float')
df9=df.iloc[:,[0,8,9]]
r=df9['漲跌(+/-)'].isin(['+'])
df9.index.names = [None]
print(df9[r])
df10=df9.sort_values('漲跌價差',ascending=False)
df10.index.names = [None]
print('漲價排行:\n',df10[r].head(50))

df15=df10.head(5)
a=df15.plot(kind='bar')
font=FontProperties(fname=r'\Windows\Fonts\msjh.ttc')
plt.xlabel('證券名稱',fontproperties=font)
plt.legend(prop=font)
plt.show()
 

#跌價排行
df11=df.iloc[:,[0,8,9]]
d=df11['漲跌(+/-)'].isin(['-'])

print(df11[d])
df12=df11.sort_values('漲跌價差',ascending=False)
df12.index.names = [None]
print('跌價排行:\n',df12[d].head(50))

#本益比排序
df['本益比'].astype('float')
df['本益比'] = df['本益比'].astype('float')
df6=df.iloc[:,[0,14]]
pe=(df['本益比']<12)
df6.index.names = [None]
print('本益比小於12:\n',df6[pe].head(50))

df8=df6.sort_values('本益比')
df8.index.names = [None]
print('本益比排序:\n',df8[pe].head(50))

##圖形化介面
from tkinter import *


def show1():
   l1['text']=df3.head(30)
def show2():
   l1['text']=df5.head(30)
def show3():
   l1['text']=df10.head(30)
def show4():
   l1['text']=df6.head(30)
def show5():
   l1['text']=df8.head(30)
    
w=Tk()
w.title('my window')
w.geometry('300x600')
w.maxsize(600,600)

b1=Button(w,text='成量排行',command=show1,bg='lightyellow',width=30)
b1['fg']='red'

b2=Button(w,text='成值排行',command=show2,bg='lightyellow',width=30)
b2['fg']='red'

b3=Button(w,text='價增排行',command=show3,bg='lightyellow',width=30)
b3['fg']='red'

b4=Button(w,text='本益比<12',command=show4,bg='lightyellow',width=30)
b4['fg']='red'

b5=Button(w,text='本益比排行',command=show5,bg='lightyellow',width=30)
b5['fg']='red'

b1.pack()
b2.pack()
b3.pack()
b4.pack()
b5.pack()

l1=Label(w,text='點選上列排行',width=30,bg='lightyellow')
l1.pack()

w.mainloop()
##簡單回測

#先安裝 用pip install backtesting

import yfinance as yf
import pandas as pd
from pandas_datareader import data
from datetime import datetime

from backtesting import Backtest, Strategy
from backtesting.lib import crossover 
from backtesting.test import SMA 

yf.pdr_override() 

target_stock = '2603.TW'  

start_date = datetime(2010, 1, 1)
end_date = datetime(2021, 12, 15) 

df = data.get_data_yahoo([target_stock], start_date, end_date)


class SmaCross(Strategy): 
    n1 = 5 #5日線 
    n2 = 20 #月線 系統帶入

    def init(self):
        self.sma1 = self.I(SMA, self.data.Close, self.n1) #設定第一條線
        self.sma2 = self.I(SMA, self.data.Close, self.n2) #設定第二條線

    def next(self):
        if crossover(self.sma1, self.sma2): 
            self.buy() #突破買入
        elif crossover(self.sma2, self.sma1): 
            self.position.close() #跌破賣出
            

stock = "2603.TW" 

df.index = pd.to_datetime(df.index) 

test = Backtest(df,SmaCross, cash=10000, commission=.002) #設定資金和手續費

result = test.run()

print(result) 

test.plot()