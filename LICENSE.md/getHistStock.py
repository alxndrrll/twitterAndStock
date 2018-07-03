# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 11:48:44 2018

Get Historical Stock Data since 2011 based on Stocksymbol of the alphavantage Data API

@author: Kalina
"""
import requests 
import pandas as pd
import mysql.connector
import sys
from dateutil.parser import parse
import datetime
  
symbol=sys.argv[1]

cnx=mysql.connector.connect(user='root',password='HTW-Berlin',host='localhost',database='stock')
cursor = cnx.cursor()
cnx.database ='stock' 

start_date=datetime.datetime(2011, 1, 1)

API_KEY = 'XR919OQRJ4ME1S30'
r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+ symbol +'&outputsize=full&apikey=' + API_KEY)
print(r)
if (r.status_code == 200): 
    ergebnis = r.json()
    ein=ergebnis['Time Series (Daily)']
    df=pd.DataFrame(ein)
    df=df.transpose()
    format_str = """
    INSERT INTO stock_hist(timestamp, fk_brand, open, high, low, close, volume)
    VALUES('{timestamp}', '{symbol}', '{hey}', '{high}', '{low}', '{close}', '{volume}'
    );"""
    for index, row in df.iterrows():
        try:
            if(parse(index) > start_date):
                timestamp=parse(index)
                sql_command=format_str.format(timestamp=timestamp, symbol=symbol, hey=row["1. open"], high=row["2. high"], low=row["3. low"], close=row["4. close"], volume=row["5. volume"])
                cursor.execute(sql_command)
                cnx.commit()
                print(symbol + " added " + str(index)+ " open: "+ str(row["1. open"]))
            else:
                print('didnt add date:' + str(index))
                continue       
        except mysql.connector.errors.IntegrityError as e:
            print(e.msg)
            pass

cursor.close()
cnx.close()
    
    