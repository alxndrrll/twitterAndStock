# -*- coding: utf-8 -*-
"""
Created on Wed May 30 18:55:05 2018
Set Up DB for Tweets
@author: Kalina
"""
import mysql.connector
from mysql.connector import errorcode
cnx=mysql.connector.connect(user='project',password='HTW-Berlin',host='localhost',database='stock')

cursor = cnx.cursor()
cnx.database ='stock'



#############################################################
######   Create Tables                    ################### 
#############################################################

create_people = """
CREATE TABLE IF NOT EXISTS people ( 
person_id INTEGER PRIMARY KEY AUTO_INCREMENT, 
twitter_tag VARCHAR(50) NOT NULL,
people_name VARCHAR(300)
);"""

cursor.execute(create_people)
print("created people table")

sql_command = """
CREATE TABLE IF NOT EXISTS sector ( 
sector_id INTEGER PRIMARY KEY AUTO_INCREMENT, 
sector_name VARCHAR(20) NOT NULL
);"""

cursor.execute(sql_command)
print("created table sector")

sql_command = """
CREATE TABLE IF NOT EXISTS brand ( 
brandshort VARCHAR(20) NOT NULL,
fullname VARCHAR(300),
fk_sector INTEGER NOT NULL,
PRIMARY KEY (brandshort),
FOREIGN KEY (fk_sector) REFERENCES sector(sector_id)
);"""

cursor.execute(sql_command)
print("created table brands")


drop_table = """
DROP TABLE IF EXISTS tweets;
"""
cursor.execute(drop_table)
print("dropped table")

create_tweets="""
CREATE TABLE IF NOT EXISTS tweets (
tweet_id INTEGER PRIMARY KEY AUTO_INCREMENT, 
tweet_text TEXT,
tweet_timestamp VARCHAR(300) NOT NULL,
fk_person INTEGER NOT NULL,
FOREIGN KEY (fk_person) REFERENCES people(person_id)
);"""

cursor.execute(create_tweets)
print("created tweet table")

create_stock_intra="""
CREATE TABLE IF NOT EXISTS stock_intra (
timestamp DATETIME NOT NULL,
fk_brand VARCHAR(20) NOT NULL,
open FLOAT(10,4) NOT NULL, 
high FLOAT(10,4) NOT NULL, 
low FLOAT(10,4) NOT NULL, 
close FLOAT(10,4) NOT NULL, 
volume INTEGER NOT NULL,
PRIMARY KEY (timestamp, fk_brand),
FOREIGN KEY (fk_brand) REFERENCES brand (brandshort)
);"""

cursor.execute(create_stock_intra)
print("created stock intra table")


create_sector_intra="""
CREATE TABLE IF NOT EXISTS sector_intra (
timestamp DATETIME NOT NULL,
fk_sector INTEGER NOT NULL,
points FLOAT(10,4) NOT NULL, 
PRIMARY KEY (timestamp, fk_sector),
FOREIGN KEY (fk_sector) REFERENCES sector(sector_id)
);"""

cursor.execute(create_sector_intra)
print("created sector intra table")

create_stock_hist="""
CREATE TABLE IF NOT EXISTS stock_hist (
timestamp DATE NOT NULL,
fk_brand VARCHAR(20) NOT NULL,
open FLOAT(10,4) NOT NULL, 
high FLOAT(10,4) NOT NULL, 
low FLOAT(10,4) NOT NULL, 
close FLOAT(10,4) NOT NULL, 
volume INTEGER(20) NOT NULL,
PRIMARY KEY (timestamp, fk_brand),
FOREIGN KEY (fk_brand) REFERENCES brand (brandshort)
);"""

cursor.execute(create_stock_hist)
print("created stock Historical table")

# never forget this, if you want the changes to be saved:
cursor.close()
cnx.close()
