# -*- coding: utf-8 -*-
"""
Created on Mon Mai 13 14:48:56 2018

Get minutely refreshed Sector Data based on Stocksymbol via the alphavantage Data API

@author: Kalina
"""
import requests 
import datetime
import time
import mysql.connector
import sys
from bs4 import BeautifulSoup

#######build connector#######################
cnx=mysql.connector.connect(user='root',password='HTW-Berlin',host='localhost',database='stock')
cursor = cnx.cursor()
cnx.database ='stock'  

##############get sector Data##############################

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
x=1
while(x < 60):
    getSectorData(sector_name, sectornumber)
    x+=1
    time.sleep(60)
    print('1 min over')
cursor.close()
cnx.close()
    
