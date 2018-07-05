-------------------Unfinished Version------------------------
<br>
<br>
We are just updating the last links, so wait maybe a day or 2 until you clone<br>

<b>twitterAndStock</b><br>
<br>
During a project at HTW Berlin my team <b>Kristina Spiegel and Alexander Röll</b> created a projekt in 'Unternehmenssoftware' to see if tweets could impact the stock market. <br>

<h1> Have tweets impacted the share price of a company?
<br>
<br>
<b>Used Stack while Development</b>: <br>
Ubuntu Server: Server version: 5.7.22-0ubuntu0.16.04.1 <br>
Mysql Database: mysql  Ver 14.14 Distrib 5.7.22, for Linux (x86_64) using  EditLine wr<br>
Python 3.5.2<br>

<b>Starting Point</b> <br>
SetUp Create Database and Basic Data (e.g. Sectors & Companies) with "create.py" and "fill.py"
<br>
<h2> Stock Data
Get your API key on https://www.alphavantage.co<br>

<b>Historical Stock Data</b> <br>
Get Historical Daily Data Stock Data: getHistStock.py {stocksymbol}

**Current Stock Data** <br>
getStockData.py - gets 1 hour back minutely based data for as long as the variable hours in the script defines ist.
getSectorData.py - gets minuetly based sectordata from https://www.tradingview.com/markets/indices/quotes-snp/

<H2> Twitter Data
<br>
<b>Automatize Scripts </b> <br>
In DB Table with followed people "people"
Crontab sync new tweets every.... with Script ...
if a company is found the minutely based syncing of Brand and refering Sector Data based on Stocksymbol is started getSectorData.py getStockData.py
<br>
<b>Viualisation in Tableau</b><br>
Calculation of  running standard deviation 
<t>WINDOW_AVG(AVG([vol]), -20, 0)+WINDOW_STDEV(AVG([vol]), -20, 0)
<br>
<b>Visualisation in python</b><br>
Automating plots with numpy and matplotlib 
Scripts:
main.py
visualisation.py
sql.py
