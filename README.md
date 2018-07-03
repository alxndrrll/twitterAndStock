twitterAndStock
During a project at HTW Berlin my team Kristina Spiegel and Alexander Röll created a projekt to see if tweets could impact the stock market. Have tweets impacted the share price of a company?

USWS HTW Berlin SoSe 2018 Group: Kristina Spiegel, s0553423@htw-berlin.de Alexander Röll, s0554705@htw-berlin.de Kalina Sperber, s0554634@htw-berlin.de

<b>Used Stack while Development</b>: 
Ubuntu Server: Server version: 5.7.22-0ubuntu0.16.04.1 
Mysql Database: mysql  Ver 14.14 Distrib 5.7.22, for Linux (x86_64) using  EditLine wr
Python 3.5.2


-------- All files are in Folder "scripts"------ 
SetUp Create Database and Basic Data (e.g. Sectors & Companies) with "create.py" and "fill.py"

---------Historical Analysis--------------------

Get Historical Daily Data Stock Data: /home/sperber/anaconda3/bin/python3 getHistStock.py HOG

---------Automatize Scripts --------------------

In DB Table with followed people "people"
Crontab sync new tweets every.... with Script ...
if a company is found the minutely based syncing of Brand and refering Sector Data based on Stocksymbol is started getSectorData.py getStockData.py
