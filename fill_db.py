# -*- coding: utf-8 -*-
"""
Created on Tue May 29 15:20:11 2018

@author: Kalina
"""
import requests 
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import errorcode
cnx=mysql.connector.connect(user='project',password='HTW-Berlin',host='localhost',database='stock')

cursor = cnx.cursor()
cnx.database ='stock'
cnx.autocommit = True

#############################################################
######   Fill Tables                      ################### 
######   Sektors                          ################### 
#############################################################
url= 'https://www.tradingview.com/markets/indices/quotes-snp/'
page = requests.get(url).content
soup = BeautifulSoup(page, 'lxml')
i=0
sectors =list()
sektoren=list()
nextName=True
while(nextName):
    #//*[@id="js-screener-container"]/div[4]/table/tbody/tr[1]/td[1]/div/a
    liste=soup.body.find(id="js-screener-container").find_all('div', recursive=False)[0].find("table").find("tbody").find_all("tr")[i].find_all("td")[0]
    short=liste.find("a").get_text()
    print(short)
    format_str = """INSERT INTO sector (sector_id, sector_name)
    VALUES (NULL, "{first}");"""
    sql_command=format_str.format(first=short)
   
    cursor.execute(sql_command)
    cnx.commit()
    print("has executed")
    i+=1
    try:
        if liste.find_next("tr"):
            nextName= True
        else:
            nextName = False
    except IndexError:
        print('Warning: IndexError')
        nextName = False
#############################################################
######   Fill Tables                      ################### 
######   Brand                            ################### 
#############################################################
query = """
select sector_id, 
       sector_name
  from sector
        """
cursor.execute(query)
result = cursor.fetchall()
for row in result:
    if row[1] not in ['SPF','S5TELS']:
        x=row[0]
        print(x)
        print(row[1])
        url= 'https://www.tradingview.com/symbols/SP-' +row[1] + '/components/'
        page = requests.get(url).content
        soup = BeautifulSoup(page, 'lxml')
        i=0
        nextName=True
        while(nextName):
            liste=soup.body.find(id="js-screener-container").find_all('div', recursive=False)[0].find("table").find("tbody").find_all("tr")[i].find_all("td")[0]
            name=liste.find("a").get_text()
            full_name=liste.full_name=liste.find("span").get_text().strip()
            print(name +" " +full_name)
            format_str = """INSERT INTO brand (brandshort, fullname, fk_sector)
            VALUES ("{first}", "{full_name}", "{third}");"""
            sql_command=format_str.format(first=name, full_name=full_name, third=x)
        
            cursor.execute(sql_command)
            cnx.commit()
            print("has executed")
            i+=1
            try:
                if liste.find_next("tr"):
                    nextName= True
                else:
                    nextName = False
            except IndexError:
                print('Warning: IndexError')
                nextName = False   
    
#############################################################
######   Fill Tables                      ################### 
######   People                           ################### 
#############################################################
persons = ['@realDonaldTrump','@XiJingpingReal','@PutinRF_Eng','@AngelaMerkelCDU','@JeffBezos','@Pontifex','@BillGates',
'@narendramodi','@EmmanuelMacron','@elonmusk','@WarrenBuffett','@Official_Markfb','@theresa_may','@China_Prime','@khamenei_ir','@DraghiBCE','@emo_jamie_dimon','@carlosslim']

for p in persons:
    print(p)
    format_str = """INSERT INTO people (person_id , twitter_tag , people_name)
    VALUES (NULL, "{first}", NULL);"""
    sql_command=format_str.format(first=p)
    cursor.execute(sql_command)
    cnx.commit()
    print("has executed")
                    
                
cnx.commit()
cursor.close()
cnx.close()