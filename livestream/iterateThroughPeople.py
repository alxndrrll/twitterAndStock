#!/usr/bin/env python3

################################ imports #######################################
import mysql.connector
from mysql.connector import errorcode
import subprocess
import shlex
import time

########################### build environment ##################################

# mysql conntection

cnx=mysql.connector.connect(user='root',password='HTW-Berlin',host='localhost',database='stock')
cursor = cnx.cursor()
cnx.database ='stock'

################################ define functions ##############################

def start() :
  cursor.execute('SELECT twitter_tag, person_id FROM people')
  for row in cursor.fetchall() :  
    print(row)
    if row[0] is not 210 :
      person = row[0]
      subprocess.call(shlex.split('/home/sperber/scripts/live_stream/startStream.sh ' + person))
    time.sleep(120)

start()
