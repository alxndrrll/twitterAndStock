# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 11:48:44 2018

Get minutely refreshed Stock Data based on Stocksymbol via the alphavantage Data API
The data is "delivered" in 1hour steps, and runs for as many hours as "hours" is set

@author: Kalina
"""
import requests 
import pandas as pd
import mysql.connector
import datetime
import time
import sys
import subprocess
import shlex
from bs4 import BeautifulSoup

#######build connector#######################
cnx=mysql.connector.connect(user='root',password='HTW-Berlin',host='localhost',database='stock')
cursor = cnx.cursor()
cnx.database ='stock'    

hours=12

def getSectorByBrand(symbol):
    query = """select sector.sector_id, sector.sector_name 
    from brand 
    inner join sector on brand.fk_sector = sector.sector_id 
    where brand.brandshort = '{symbol}'"""

    cursor.execute(query.format(symbol=symbol))
    result=cursor.fetchall()
    sectornumber=0
    sectorname='hi'
    for row in result:
        return (row[0], row[1])


def getSectorData(sector_name, sectornumber):
    url= 'https://www.tradingview.com/markets/indices/quotes-snp/'
    page = requests.get(url).content
    soup = BeautifulSoup(page, 'lxml')
    liste=soup.body.find(id="js-screener-container").find_all('div', recursive=False)[0].find("table").find("tbody").find_all("tr")[int(sectornumber)-67].find_all("td")[1]
    kurs=liste.get_text()
    print(kurs)
    #####get timestamp###########
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    #####save data#####
    format_str = """
    INSERT INTO sector_intra(timestamp, fk_sector, points)
    VALUES('{timestamp}', '{sector_id}', '{test}'
    );"""
    sql_command=format_str.format(timestamp=st, sector_id=sectornumber, test=kurs)
    cursor.execute(sql_command)
    cnx.commit()

symbol=sys.argv[1]
print(symbol)
sectornumber, sector_name= getSectorByBrand(symbol)
print(sector_name )
print(sectornumber)
getSectorData(sector_name, sectornumber)
def getStockData(symbol):
    API_KEY = 'XR919OQRJ4ME1S30'
    r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=' + symbol + '&interval=1min&apikey=' + API_KEY)
    if (r.status_code == 200):
        print( "status 200 all good")
    
    ergebnis = r.json()
    #print(ergebnis)
    ein=ergebnis['Time Series (1min)']
    df=pd.DataFrame(ein)
    df=df.transpose()
    format_str = """
    INSERT INTO stock_intra(timestamp, fk_brand, open, high, low, close, volume)
    VALUES('{timestamp}', '{symbol}', '{hey}', '{high}', '{low}', '{close}', '{volume}'
    );"""
    for index, row in df.iterrows():
        try:
            print("Data for "+ str(symbol) + " open: " +str(row["1. open"]))
            sql_command=format_str.format(timestamp=index, symbol=symbol, hey=row["1. open"], high=row["2. high"], low=row["3. low"], close=row["4. close"], volume=row["5. volume"])
            cursor.execute(sql_command)
            cnx.commit()
        except mysql.connector.errors.IntegrityError as e:
            print("This Data already exists in Table")

symbol=sys.argv[1]
print(symbol)
x=1
while(x < hours):
    getStockData(symbol)
    subprocess.call(shlex.split('/home/sperber/anaconda3/bin/python3 getSectorData.py ' + symbol))
    x+=1
    time.sleep(3600)
    print('1 hour over')

cursor.close()
cnx.close()
    
    
    
